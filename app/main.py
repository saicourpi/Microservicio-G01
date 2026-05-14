from fastapi import FastAPI, Query, HTTPException
from fastapi.middleware.cors import CORSMiddleware
import pandas as pd
import os
import unicodedata

app = FastAPI(
    title="Sistema de Recomendación Agrícola",
    version="5.0"
)

# =========================
# CORS
# =========================

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# =========================
# LIMPIAR TEXTO
# =========================

def limpiar_texto(texto):

    if pd.isna(texto):
        return ""

    texto = str(texto).strip().upper()

    texto = unicodedata.normalize('NFKD', texto)
    texto = texto.encode('ASCII', 'ignore').decode('utf-8')

    return texto

# =========================
# LEER DATASET
# =========================

file_path = "DATASET_MAESTRO_ML.xlsx"

if not os.path.exists(file_path):
    raise FileNotFoundError("No se encontró el dataset.")

# Leer excel
df = pd.read_excel(file_path)

# Limpiar columnas
df.columns = df.columns.str.strip().str.lower()

# MOSTRAR COLUMNAS
print("COLUMNAS DETECTADAS:")
print(df.columns.tolist())

# =========================
# COLUMNAS NUMERICAS
# =========================

columnas_numericas = [
    "anio",
    "produccion_t",
    "temp_max",
    "temp_min",
    "precipitacion"
]

for col in columnas_numericas:

    if col in df.columns:
        df[col] = pd.to_numeric(df[col], errors="coerce")

# =========================
# LIMPIAR COLUMNAS TEXTO
# =========================

columnas_texto = [
    "dpto",
    "prov",
    "dist",
    "cultivo"
]

for col in columnas_texto:

    if col in df.columns:
        df[col] = df[col].apply(limpiar_texto)

# Convertir año entero
df["anio"] = df["anio"].astype(int)

print(df.head())

# =========================
# API
# =========================

@app.get("/recomendar-cultivo")
def recomendar_cultivo(

    anio: int = Query(...),

    departamento: str = Query(...),

    provincia: str = Query(...),

    distrito: str = Query(...)
):

    departamento = limpiar_texto(departamento)
    provincia = limpiar_texto(provincia)
    distrito = limpiar_texto(distrito)

    print("BUSCANDO:")
    print(anio, departamento, provincia, distrito)

    # =========================
    # FILTRO
    # =========================

    filtro = df[

        (df["anio"] == anio) &

        (df["dpto"] == departamento) &

        (df["prov"] == provincia) &

        (df["dist"] == distrito)

    ]

    print("TOTAL ENCONTRADOS:")
    print(len(filtro))

    if filtro.empty:

        raise HTTPException(
            status_code=404,
            detail="No existen datos para la ubicación indicada."
        )

    # Ordenar por producción
    filtro = filtro.sort_values(
        by="produccion_t",
        ascending=False
    )

    resultados = []

    for _, row in filtro.iterrows():

        resultados.append({

            "anio": int(row["anio"]),

            "departamento": row["dpto"],

            "provincia": row["prov"],

            "distrito": row["dist"],

            "cultivo": row["cultivo"],

            "produccion_t": round(
                float(row.get("produccion_t", 0)), 2
            ),

            "temp_max": round(
                float(row.get("temp_max", 0)), 2
            ),

            "temp_min": round(
                float(row.get("temp_min", 0)), 2
            ),

            "precipitacion": round(
                float(row.get("precipitacion", 0)), 2
            ),

            "superficie_cosechada_ha": round(
                float(row.get("superficie_cosechada_ha", 0)), 2
            ),

            "rendimiento_t_ha": round(
                float(row.get("rendimiento_t_ha", 0)), 2
            )

        })

    return {

        "total_cultivos": len(resultados),

        "resultados": resultados

    }