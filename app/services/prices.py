import pandas as pd
import os

class MotorPrecios:
    def __init__(self):
        print(" Inicializando el Motor de Tendencia de Precios...")
        directorio_actual = os.path.dirname(os.path.abspath(__file__))
        ruta_csv = os.path.join(directorio_actual, "..", "..", "data", "dataset_agroclima.csv")
        self.df_clima = pd.read_csv(ruta_csv)
        self.df_clima.columns = self.df_clima.columns.str.strip().str.lower()
        print("Data histórica cargada para precios.")

    def estimar_tendencia(self, dpto: str, prov: str, dist: str, cultivo: str):
        dpto = dpto.strip().upper()
        prov = prov.strip().upper()
        dist = dist.strip().upper()
        cultivo = cultivo.strip().upper()

        # 1. Filtramos la data
        filtro = self.df_clima[
            (self.df_clima['dpto'] == dpto) &
            (self.df_clima['prov'] == prov) &
            (self.df_clima['dist'] == dist) &
            (self.df_clima['cultivo'] == cultivo)
        ]

        if filtro.empty:
            raise ValueError(f"No hay registros de precios para {cultivo} en {dist}.")

        # 2. Agrupamos por año y sacamos el precio promedio
        precio_anual = filtro.groupby('anio')['precio_chacra'].mean().reset_index().sort_values('anio')

        # Si solo tenemos 1 año de datos, no podemos calcular una tendencia
        if len(precio_anual) < 2:
            precio_unico = precio_anual.iloc[0]['precio_chacra']
            return {
                "tendencia_general": "ESTABLE ⚖️",
                "variacion_porcentual": "0.0%",
                "precio_mas_reciente": round(precio_unico, 2),
                "historial": [{"anio": int(precio_anual.iloc[0]['anio']), "precio": round(precio_unico, 2)}]
            }

        # 3. Calculamos la variación entre el primer y último año
        primer_anio = precio_anual.iloc[0]
        ultimo_anio = precio_anual.iloc[-1]

        precio_inicial = primer_anio['precio_chacra']
        precio_final = ultimo_anio['precio_chacra']

        # Evitamos divisiones por cero por si acaso
        if precio_inicial == 0:
            variacion = 0.0
        else:
            variacion = ((precio_final - precio_inicial) / precio_inicial) * 100

        # 4. Asignamos la tendencia visual
        if variacion > 5:
            tendencia = "AL ALZA 📈"
        elif variacion < -5:
            tendencia = "A LA BAJA 📉"
        else:
            tendencia = "ESTABLE ⚖️"

        # 5. Preparamos el historial para que la web pueda dibujar un grafiquito después
        historial = []
        for _, row in precio_anual.iterrows():
            historial.append({
                "anio": int(row['anio']),
                "precio_promedio": round(row['precio_chacra'], 2)
            })

        return {
            "tendencia_general": tendencia,
            "variacion_porcentual": f"{round(variacion, 2)}%",
            "precio_mas_reciente": round(precio_final, 2),
            "historial": historial
        }

# Instanciamos el motor
motor_precios = MotorPrecios()