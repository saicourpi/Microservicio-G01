from fastapi import FastAPI, Query, HTTPException
import pandas as pd
import os
from typing import Dict, List, Any
import logging

# Configuración de logging para trazabilidad en producción
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("agro_microservice")

app = FastAPI(
    title="Microservicio de Recomendación Agrícola - Lambayeque",
    description="Determina el cultivo óptimo según condiciones históricas de temperatura y precipitación por provincia y distrito.",
    version="1.0.0"
)

# Variable global para evitar recargas innecesarias del DataFrame
_df_cache: pd.DataFrame | None = None

def load_and_clean_dataset() -> pd.DataFrame:
    """Carga y sanea el dataset agrícola-climático."""
    global _df_cache
    file_path = "Lambayeque_AgroClima.xlsx"
    
    if not os.path.exists(file_path):
        raise FileNotFoundError(f"Dataset no encontrado en la ruta: {file_path}")
        
    df = pd.read_excel(file_path)
    
    # 1. Normalización de nombres de columnas
    df.columns = df.columns.str.strip()
    
    # 2. Coerción de tipos numéricos críticos
    numeric_cols = ['temp_max_promedio', 'temp_min_promedio', 'precipitacion_total', 'PRODUCCION(t)']
    for col in numeric_cols:
        df[col] = pd.to_numeric(df[col], errors='coerce')
        
    # 3. Eliminación de registros inválidos o sin producción registrada
    df = df.dropna(subset=['provincia', 'distrito', 'dsc_Cultivo', 'PRODUCCION(t)'])
    df = df[df['PRODUCCION(t)'] > 0]  # Filtra cosechas fallidas o no cuantificadas
    
    _df_cache = df.copy()
    logger.info("Dataset cargado y saneado correctamente.")
    return df

@app.on_event("startup")
def startup_event():
    load_and_clean_dataset()

@app.get("/recomendar-cultivo", response_model=Dict[str, Any])
def recomendar_cultivo(
    provincia: str = Query(..., description="Nombre de la provincia (ej. CHICLAYO)"),
    distrito: str = Query(..., description="Nombre del distrito (ej. CHICLAYO)")
):
    """
    Recomienda el cultivo con mayor rendimiento histórico en la ubicación especificada,
    junto con las condiciones climáticas promedio bajo las cuales prosperó.
    """
    if _df_cache is None:
        raise HTTPException(status_code=500, detail="Dataset no inicializado correctamente.")

    # Filtro geográfico insensible a mayúsculas/minúsculas y espacios residuales
    mask = (
        (_df_cache['provincia'].str.upper().str.strip() == provincia.upper().strip()) &
        (_df_cache['distrito'].str.upper().str.strip() == distrito.upper().strip())
    )
    
    df_loc = _df_cache[mask]
    
    if df_loc.empty:
        raise HTTPException(status_code=404, detail="No existen registros históricos para la provincia y distrito indicados.")

    # Agregación estadística por cultivo
    crop_metrics = df_loc.groupby('dsc_Cultivo').agg(
        produccion_promedio=('PRODUCCION(t)', 'mean'),
        produccion_maxima=('PRODUCCION(t)', 'max'),
        temp_max_promedio=('temp_max_promedio', 'mean'),
        temp_min_promedio=('temp_min_promedio', 'mean'),
        precipitacion_promedio=('precipitacion_total', 'mean'),
        n_registros=('PRODUCCION(t)', 'count')
    ).reset_index()

    # Orden descendente por rendimiento histórico
    crop_metrics = crop_metrics.sort_values('produccion_promedio', ascending=False).reset_index(drop=True)
    
    # Extracción del cultivo óptimo
    top_crop = crop_metrics.iloc[0]
    
    return {
        "ubicacion": {"provincia": provincia, "distrito": distrito},
        "cultivo_optimo": top_crop['dsc_Cultivo'],
        "rendimiento_historico_tn": round(top_crop['produccion_promedio'], 2),
        "rango_rendimiento_tn": {
            "min": round(crop_metrics['produccion_promedio'].min(), 2),
            "max": round(top_crop['produccion_maxima'], 2)
        },
        "condiciones_climaticas_asociadas": {
            "temp_max_media_c": round(top_crop['temp_max_promedio'], 2),
            "temp_min_media_c": round(top_crop['temp_min_promedio'], 2),
            "precipitacion_media_mm": round(top_crop['precipitacion_promedio'], 2)
        },
        "top_3_alternativas": crop_metrics.head(3)[['dsc_Cultivo', 'produccion_promedio', 'n_registros']].to_dict(orient='records'),
        "nota_metodologica": "La recomendación se basa en el rendimiento histórico promedio (PRODUCCION(t)) bajo las condiciones climáticas registradas en el dataset. Para una predicción prospectiva, se sugiere integrar un modelo de regresión multivariada o árboles de decisión."
    }

from fastapi.middleware.cors import CORSMiddleware

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)