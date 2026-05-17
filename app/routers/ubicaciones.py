from fastapi import APIRouter
from app.services.locations import motor_ubicaciones

router = APIRouter(
    prefix="/api/ubicaciones",
    tags=["Ubicaciones Dinámicas"]
)

@router.get("/jerarquia")
def obtener_jerarquia():
    # Devolvemos el árbol completo para que el Frontend haga los filtros en milisegundos
    return motor_ubicaciones.jerarquia