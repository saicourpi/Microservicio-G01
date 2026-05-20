from fastapi import APIRouter, Query, HTTPException
from app.services.predictor import motor_ia

router = APIRouter(
    prefix="/api/cultivos",
    tags=["Recomendaciones Agrícolas"]
)

@router.get("/recomendar")
def recomendar_cultivo(
    dpto: str = Query(..., description="Departamento (Ej. ICA)"),
    prov: str = Query(..., description="Provincia (Ej. ICA)"),
    dist: str = Query(..., description="Distrito (Ej. LA TINGUINA)")
):
    try:
        # ¡Solo le pasamos los 3 datos, el motor se encarga del resto! 🤖✨
        resultados = motor_ia.predecir_top_3(dpto=dpto, prov=prov, dist=dist)
        
        return {
            "estado": "éxito",
            "mensaje": "¡Predicción realizada autocompletando el clima histórico!",
            "data": resultados
        }
        
    except ValueError as e:
        # Error 404 si el distrito no existe en la data
        raise HTTPException(
            status_code=404, 
            detail=str(e)
        )
    except Exception as e:
        raise HTTPException(
            status_code=500, 
            detail=f"Hubo un error en la predicción: {str(e)}"
        )