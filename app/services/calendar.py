import pandas as pd
import os

class MotorCalendario:
    def __init__(self):
        print("📅 Inicializando el Motor de Calendario de Siembra...")
        
        # Cargamos nuestra data histórica
        directorio_actual = os.path.dirname(os.path.abspath(__file__))
        ruta_csv = os.path.join(directorio_actual, "..", "..", "data", "dataset_agroclima.csv")
        
        self.df_clima = pd.read_csv(ruta_csv)
        self.df_clima.columns = self.df_clima.columns.str.strip().str.lower()
        print("✅ Data histórica cargada para el calendario.")

    def obtener_mejores_meses(self, dpto: str, prov: str, dist: str, cultivo: str):
        dpto = dpto.strip().upper()
        prov = prov.strip().upper()
        dist = dist.strip().upper()
        cultivo = cultivo.strip().upper()

        # 1. Filtramos por la ubicación y el cultivo exacto
        filtro = self.df_clima[
            (self.df_clima['dpto'] == dpto) &
            (self.df_clima['prov'] == prov) &
            (self.df_clima['dist'] == dist) &
            (self.df_clima['cultivo'] == cultivo)
        ]

        if filtro.empty:
            raise ValueError(f"No hay registros históricos suficientes para {cultivo} en {dist}.")

        # 2. Agrupamos por mes y sacamos el promedio del rendimiento (kg/ha)
        rendimiento_mensual = filtro.groupby('mes')['rendimiento_kgha'].mean().reset_index()
        
        # 3. Ordenamos de mayor a menor rendimiento
        rendimiento_mensual = rendimiento_mensual.sort_values(by='rendimiento_kgha', ascending=False)
        
        # 4. Un toque de Senior de UX: Mapeamos los números a nombres de meses
        nombres_meses = {
            1: "Enero", 2: "Febrero", 3: "Marzo", 4: "Abril",
            5: "Mayo", 6: "Junio", 7: "Julio", 8: "Agosto",
            9: "Septiembre", 10: "Octubre", 11: "Noviembre", 12: "Diciembre"
        }

        # 5. Sacamos el Top 3
        top_3 = rendimiento_mensual.head(3)
        
        meses_recomendados = []
        for _, row in top_3.iterrows():
            mes_num = int(row['mes'])
            meses_recomendados.append({
                "mes_numero": mes_num,
                "mes_nombre": nombres_meses.get(mes_num, "Desconocido"),
                "rendimiento_historico_kgha": round(row['rendimiento_kgha'], 2)
            })

        return meses_recomendados

# Instanciamos el motor para que FastAPI lo use
motor_calendario = MotorCalendario()