from fastapi import APIRouter, Query, HTTPException
from app.services.prices import motor_precios

router = APIRouter(
    prefix="/api/precios",
    tags=["Tendencia de Precios"]
)

@router.get("/tendencia")
def tendencia_precios(
    dpto: str = Query(..., description="Departamento"),
    prov: str = Query(..., description="Provincia"),
    dist: str = Query(..., description="Distrito"),
    cultivo: str = Query(..., description="Nombre del Cultivo (Ej. MAIZ_AMARILLO_DURO)")
):
    try:
        resultado = motor_precios.estimar_tendencia(dpto, prov, dist, cultivo)
        
        return {
            "estado": "éxito",
            "ubicacion": dist,
            "cultivo": cultivo,
            "datos_economicos": resultado
        }
        
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))