#el servicio en Python que va a leer el Excel, limpiará los nombres y armará una estructura de árbol para que la API 
#pueda responder con las provincias y distritos disponibles según el departamento que el agricultor seleccione. Esto es súper
# útil para evitar errores de tipeo y mejorar la experiencia del usuario.

import pandas as pd
import os

class MotorUbicaciones:
    def __init__(self):
        print("🗺️ Inicializando el Motor de Ubicaciones Dinámicas...")
        
        # Cargamos el archivo CSV
        directorio_actual = os.path.dirname(os.path.abspath(__file__))
        ruta_csv = os.path.join(directorio_actual, "..", "..", "data", "dataset_agroclima.csv")
        
        df = pd.read_csv(ruta_csv)
        df.columns = df.columns.str.strip().str.lower()
        
        # Generamos la estructura en memoria al iniciar la API
        self.jerarquia = self._construir_jerarquia(df)
        print("✅ Jerarquía de ubicaciones generada con éxito.")

    def _construir_jerarquia(self, df):
        # Sacamos las combinaciones únicas de dpto, prov y dist
        df_unicos = df[['dpto', 'prov', 'dist']].drop_duplicates()
        
        jerarquia = {}
        
        for _, row in df_unicos.iterrows():
            dpto = str(row['dpto']).strip().upper()
            prov = str(row['prov']).strip().upper()
            dist = str(row['dist']).strip().upper()
            
            # Armamos el árbol anidado: { DEPARTAMENTO: { PROVINCIA: [DISTRITOS] } }
            if dpto not in jerarquia:
                jerarquia[dpto] = {}
            if prov not in jerarquia[dpto]:
                jerarquia[dpto][prov] = []
            if dist not in jerarquia[dpto][prov]:
                jerarquia[dpto][prov].append(dist)
                
        return jerarquia

# Instanciamos el motor
motor_ubicaciones = MotorUbicaciones()