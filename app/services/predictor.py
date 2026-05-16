import joblib
import pandas as pd
import numpy as np
import os

class AgroPredictor:
    def __init__(self):
        print(" Inicializando el Motor de Inteligencia Agrícola...")
        
        # 1. Buscamos las rutas de nuestros archivos
        directorio_actual = os.path.dirname(os.path.abspath(__file__))
        ruta_modelo = os.path.join(directorio_actual, "..", "models", "rf_cultivos.pkl")
        ruta_columnas = os.path.join(directorio_actual, "..", "models", "columnas_x.pkl")
        
        # Subimos dos niveles para llegar a la carpeta 'data'
        ruta_csv = os.path.join(directorio_actual, "..", "..", "data", "dataset_agroclima.csv")
        
        # Cargamos el modelo y columnas
        self.modelo = joblib.load(ruta_modelo)
        self.columnas_x = joblib.load(ruta_columnas)
        
        # Cargamos la data histórica a la memoria
        self.df_clima = pd.read_csv(ruta_csv)
        self.df_clima.columns = self.df_clima.columns.str.strip().str.lower()
        self.df_clima['humedad'] = self.df_clima['humedad'].fillna(self.df_clima['humedad'].mean())
        
        print(" Modelo y data histórica cargados con éxito.")

    #  no pedimos temperatura ni humedad, solo la ubicación 
    def predecir_top_3(self, dpto: str, prov: str, dist: str):
        
        dpto = dpto.strip().upper()
        prov = prov.strip().upper()
        dist = dist.strip().upper()
        
        # 1. Buscamos el distrito en nuestro dataset histórico
        filtro = self.df_clima[
            (self.df_clima['dpto'] == dpto) &
            (self.df_clima['prov'] == prov) &
            (self.df_clima['dist'] == dist)
        ]
        
        # Si el agricultor pone un distrito que no existe en nuestra data, lanzamos un error claro
        if filtro.empty:
            raise ValueError(f"No tenemos datos climáticos históricos para el distrito: {dist}")
            
        # 2. Calculamos el clima promedio histórico de ESE distrito
        altitud_promedio = filtro['altitud'].mean()
        temp_max_promedio = filtro['temp_max'].mean()
        temp_min_promedio = filtro['temp_min'].mean()
        precipitacion_promedio = filtro['precipitacion'].mean()
        humedad_promedio = filtro['humedad'].mean()

        # 3. Armamos la fila con los promedios encontrados (¡Autocompletado!)
        input_data = pd.DataFrame([{
            'dpto': dpto,
            'prov': prov,
            'dist': dist,
            'altitud': altitud_promedio,
            'temp_max': temp_max_promedio,
            'temp_min': temp_min_promedio,
            'precipitacion': precipitacion_promedio,
            'humedad': humedad_promedio
        }])

        # 4. Transformamos y ajustamos columnas para el modelo
        input_encoded = pd.get_dummies(input_data)
        input_final = input_encoded.reindex(columns=self.columnas_x, fill_value=0)

        # 5. Predicción
        probabilidades = self.modelo.predict_proba(input_final)[0]
        clases_cultivos = self.modelo.classes_
        top_3_indices = np.argsort(probabilidades)[::-1][:3]
        
        recomendaciones = []
        for idx in top_3_indices:
            prob = probabilidades[idx]
            if prob > 0:
                recomendaciones.append({
                    "cultivo": clases_cultivos[idx],
                    "probabilidad_exito": f"{round(prob * 100, 2)}%"
                })
        
        # 6. Devolvemos tanto los cultivos recomendados como el clima que usamos
        return {
            "clima_historico_utilizado": {
                "altitud_msnm": round(altitud_promedio, 2),
                "temp_max_c": round(temp_max_promedio, 2),
                "temp_min_c": round(temp_min_promedio, 2),
                "precipitacion_mm": round(precipitacion_promedio, 2),
                "humedad_pct": round(humedad_promedio, 2)
            },
            "recomendaciones": recomendaciones
        }

# Instanciamos la clase
motor_ia = AgroPredictor()