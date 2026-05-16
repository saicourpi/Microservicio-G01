import pandas as pd
import os
from datetime import datetime
#Usará matemática pura para calcular qué cultivos dan más dinero este mes:
class MotorTemporada:
    def __init__(self):
        print(" Inicializando el Motor de Oportunidades de Temporada...")
        directorio_actual = os.path.dirname(os.path.abspath(__file__))
        ruta_csv = os.path.join(directorio_actual, "..", "..", "data", "dataset_agroclima.csv")
        
        self.df_clima = pd.read_csv(ruta_csv)
        self.df_clima.columns = self.df_clima.columns.str.strip().str.lower()
        print(" Data histórica cargada para oportunidades estacionales.")

    def obtener_oportunidades_mes(self, dpto: str, prov: str, dist: str, mes: int = None):
        # 🧠 Si no le pasamos mes, detecta automáticamente el mes de la vida real
        if mes is None:
            mes = datetime.now().month 

        dpto = dpto.strip().upper()
        prov = prov.strip().upper()
        dist = dist.strip().upper()

        # 1. Filtramos por ubicación y por el mes actual
        filtro = self.df_clima[
            (self.df_clima['dpto'] == dpto) &
            (self.df_clima['prov'] == prov) &
            (self.df_clima['dist'] == dist) &
            (self.df_clima['mes'] == mes)
        ]

        if filtro.empty:
            raise ValueError(f"No hay suficientes registros históricos para el mes {mes} en {dist}.")

        # 2. Agrupamos por cultivo y sacamos el precio y rendimiento promedio de ESTE mes
        agrupado = filtro.groupby('cultivo').agg({
            'rendimiento_kgha': 'mean',
            'precio_chacra': 'mean'
        }).reset_index()

        # 3. Calculamos la rentabilidad estimada (Kilos x Precio)
        agrupado['ingreso_estimado'] = agrupado['rendimiento_kgha'] * agrupado['precio_chacra']
        
        # 4. Ordenamos de mayor a menor rentabilidad y sacamos el Top 3
        agrupado = agrupado.sort_values(by='ingreso_estimado', ascending=False)
        top_3 = agrupado.head(3)

        nombres_meses = {
            1: "Enero", 2: "Febrero", 3: "Marzo", 4: "Abril", 5: "Mayo", 6: "Junio",
            7: "Julio", 8: "Agosto", 9: "Septiembre", 10: "Octubre", 11: "Noviembre", 12: "Diciembre"
        }

        oportunidades = []
        for _, row in top_3.iterrows():
            oportunidades.append({
                "cultivo": row['cultivo'],
                "rendimiento_promedio": round(row['rendimiento_kgha'], 2),
                "precio_promedio": round(row['precio_chacra'], 2)
            })

        return {
            "mes_numero": mes,
            "mes_nombre": nombres_meses.get(mes, "Desconocido"),
            "oportunidades": oportunidades
        }

motor_temporada = MotorTemporada()