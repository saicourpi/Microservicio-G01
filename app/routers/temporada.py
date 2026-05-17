from fastapi import APIRouter, Query, HTTPException
from app.services.seasonal import motor_temporada

router = APIRouter(
    prefix="/api/temporada",
    tags=["Oportunidades Estacionales"]
)

@router.get("/oportunidades")
def obtener_oportunidades(
    dpto: str = Query(..., description="Departamento"),
    prov: str = Query(..., description="Provincia"),
    dist: str = Query(..., description="Distrito")
):
    try:
        return motor_temporada.obtener_oportunidades_mes(dpto, prov, dist)
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))