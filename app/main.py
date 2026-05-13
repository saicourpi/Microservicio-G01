from fastapi import FastAPI, Query, HTTPException
from fastapi.middleware.cors import CORSMiddleware
import pandas as pd
import os
from typing import Dict, Any
import logging

# Configuración de logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("agro_microservice")

app = FastAPI(
    title="Microservicio de Recomendación Agrícola",
    description="Recomienda el cultivo óptimo según historial agrícola y climático.",
    version="2.0.0"
)

# Cache global
_df_cache: pd.DataFrame | None = None


def load_and_clean_dataset() -> pd.DataFrame:
    """
    Carga y limpia el dataset agrícola.
    """
    global _df_cache

    file_path = "DATASET_MAESTRO_ML.xlsx"

    if not os.path.exists(file_path):
        raise FileNotFoundError(f"No se encontró el dataset: {file_path}")

    # Leer Excel
    df = pd.read_excel(file_path)

    # Limpiar nombres de columnas
    df.columns = df.columns.str.strip()

    print("COLUMNAS DEL DATASET:")
    print(df.columns)

    # Columnas numéricas del nuevo dataset
    numeric_cols = [
        'temp_max',
        'temp_min',
        'precipitacion',
        'produccion_t'
    ]

    # Convertir columnas numéricas
    for col in numeric_cols:
        df[col] = pd.to_numeric(df[col], errors='coerce')

    # Eliminar registros vacíos
    df = df.dropna(subset=[
        'prov',
        'dist',
        'cultivo',
        'produccion_t'
    ])

    # Filtrar producción válida
    df = df[df['produccion_t'] > 0]

    _df_cache = df.copy()

    logger.info("Dataset cargado correctamente.")

    return df


@app.on_event("startup")
def startup_event():
    load_and_clean_dataset()


@app.get("/recomendar-cultivo", response_model=Dict[str, Any])
def recomendar_cultivo(
    provincia: str = Query(..., description="Provincia"),
    distrito: str = Query(..., description="Distrito")
):
    """
    Recomienda el cultivo con mejor rendimiento histórico.
    """

    if _df_cache is None:
        raise HTTPException(
            status_code=500,
            detail="Dataset no cargado correctamente."
        )

    # Filtro geográfico
    mask = (
        (_df_cache['prov'].astype(str).str.upper().str.strip() == provincia.upper().strip()) &
        (_df_cache['dist'].astype(str).str.upper().str.strip() == distrito.upper().strip())
    )

    df_loc = _df_cache[mask]

    if df_loc.empty:
        raise HTTPException(
            status_code=404,
            detail="No existen datos para la ubicación indicada."
        )

    # Agrupación estadística
    crop_metrics = df_loc.groupby('cultivo').agg(
        produccion_promedio=('produccion_t', 'mean'),
        produccion_maxima=('produccion_t', 'max'),
        temp_max_promedio=('temp_max', 'mean'),
        temp_min_promedio=('temp_min', 'mean'),
        precipitacion_promedio=('precipitacion', 'mean'),
        n_registros=('produccion_t', 'count')
    ).reset_index()

    # Ordenar por mejor producción
    crop_metrics = crop_metrics.sort_values(
        by='produccion_promedio',
        ascending=False
    ).reset_index(drop=True)

    # Mejor cultivo
    top_crop = crop_metrics.iloc[0]

    return {
        "ubicacion": {
            "provincia": provincia,
            "distrito": distrito
        },

        "cultivo_optimo": top_crop['cultivo'],

        "rendimiento_historico_tn": round(
            top_crop['produccion_promedio'], 2
        ),

        "rango_rendimiento_tn": {
            "min": round(
                crop_metrics['produccion_promedio'].min(), 2
            ),
            "max": round(
                top_crop['produccion_maxima'], 2
            )
        },

        "condiciones_climaticas_asociadas": {
            "temp_max_media_c": round(
                top_crop['temp_max_promedio'], 2
            ),
            "temp_min_media_c": round(
                top_crop['temp_min_promedio'], 2
            ),
            "precipitacion_media_mm": round(
                top_crop['precipitacion_promedio'], 2
            )
        },

        "top_3_alternativas": crop_metrics.head(3)[
            ['cultivo', 'produccion_promedio', 'n_registros']
        ].to_dict(orient='records'),

        "nota_metodologica": (
            "La recomendación se basa en el rendimiento histórico "
            "promedio registrado en el dataset."
        )
    }


# Configuración CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)