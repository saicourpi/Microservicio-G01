from fastapi import APIRouter, Query, HTTPException
from app.services.calendar import motor_calendario

router = APIRouter(
    prefix="/api/calendario",
    tags=["Calendario de Siembra"]
)

@router.get("/optimo")
def calendario_optimo(
    dpto: str = Query(..., description="Departamento"),
    prov: str = Query(..., description="Provincia"),
    dist: str = Query(..., description="Distrito"),
    cultivo: str = Query(..., description="Nombre del Cultivo (Ej. MAIZ_AMARILLO_DURO)")
):
    try:
        # Llamamos a nuestro nuevo motor
        meses = motor_calendario.obtener_mejores_meses(dpto, prov, dist, cultivo)
        
        return {
            "estado": "éxito",
            "ubicacion": dist,
            "cultivo": cultivo,
            "mejores_meses": meses
        }
        
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))