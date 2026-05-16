#aqui arranca la api
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

# Importamos las rutas que acabamos de crear
from app.routers import cultivos
from app.routers import alertas
from app.routers import calendario
from app.routers import precios
from app.routers import ubicaciones
from app.routers import temporada
from app.routers import agronomia
app = FastAPI(
    title=" Sistema de Recomendación Agrícola",
    version="1.0",
    description="Microservicio con Machine Learning para predicción de cultivos y clima."
)

# =========================
# CONFIGURACIÓN CORS (¡Súper importante para el Frontend!)
# =========================
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"], # En producción, aquí pondríamos el dominio real
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# =========================
# CONECTANDO RUTAS
# =========================
app.include_router(cultivos.router)
app.include_router(alertas.router)
app.include_router(agronomia.router)

@app.get("/")
def read_root():
    return {
        "mensaje": "¡Bienvenida a la API de Recomendación Agroclimática! El servidor está corriendo perfectamente."
    }