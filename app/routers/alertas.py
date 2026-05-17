from fastapi import APIRouter, Query, HTTPException
from app.services.predictor import motor_ia
from app.services.rules import motor_alertas

router = APIRouter(
    prefix="/api/alertas",
    tags=["Alertas Agroclimáticas"]
)

@router.get("/evaluar")
def evaluar_estres(
    dpto: str = Query(..., description="Departamento"),
    prov: str = Query(..., description="Provincia"),
    dist: str = Query(..., description="Distrito")
):
    try:
        # 1. Le pedimos prestado al Motor IA el clima histórico del distrito
        datos_ia = motor_ia.predecir_top_3(dpto=dpto, prov=prov, dist=dist)
        clima = datos_ia["clima_historico_utilizado"]

        # 2. Pasamos esos números por nuestro Motor de Alertas
        alertas = motor_alertas.evaluar_clima(
            temp_max=clima["temp_max_c"],
            temp_min=clima["temp_min_c"],
            precipitacion=clima["precipitacion_mm"],
            humedad=clima["humedad_pct"]
        )

        return {
            "estado": "éxito",
            "ubicacion": dist,
            "alertas": alertas
        }
        
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))