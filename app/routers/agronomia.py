from fastapi import APIRouter, Query
from app.services.agronomy import motor_agronomico

router = APIRouter(
    prefix="/api/agronomia",
    tags=["Fichas Agronómicas"]
)

@router.get("/ficha")
def obtener_ficha_tecnica(cultivo: str = Query(..., description="Nombre del cultivo")):
    # Aquí es donde el router llama al "cerebro" que acabamos de crear
    return motor_agronomico.obtener_ficha(cultivo)