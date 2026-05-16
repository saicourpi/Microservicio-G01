import pandas as pd
import os
#Le damos al modelo el 80% de los datos para que estudie (entrene) y nos guardamos el 20% para tomarle un examen y ver si realmente aprendió a predecir cultivos.
from sklearn.model_selection import train_test_split
#Creamos 100 "árboles de decisión" (n_estimators=100) para que voten juntos cuál es el mejor cultivo.
from sklearn.ensemble import RandomForestClassifier
#Guardamos tanto el modelo (rf_cultivos.pkl) como la estructura de las columnas (columnas_x.pkl). Esto es crucial para que la API pueda usar el modelo correctamente cuando un agricultor consulte.
import joblib

# 1. Configuramos nuestras rutas dinámicas
directorio_script = os.path.dirname(os.path.abspath(__file__))
ruta_csv = os.path.join(directorio_script, "..", "data", "dataset_agroclima.csv")
# Aquí guardaremos el modelo entrenado y las columnas
ruta_modelo = os.path.join(directorio_script, "..", "app", "models", "rf_cultivos.pkl")
ruta_columnas = os.path.join(directorio_script, "..", "app", "models", "columnas_x.pkl")

print(" Cargando el dataset...")

try:
    # 2. Carga y limpieza inicial
    df = pd.read_csv(ruta_csv)
    df.columns = df.columns.str.strip().str.lower()
    
    print("🧹 Limpiando los datos...")
    # Rellenamos los huecos de humedad con el promedio
    df['humedad'] = df['humedad'].fillna(df['humedad'].mean())
    
    # 3. Separamos nuestras Features (X) y el Target (y)
    columnas_x = ['dpto', 'prov', 'dist', 'altitud', 'temp_max', 'temp_min', 'precipitacion', 'humedad']
    X = df[columnas_x]
    y = df['cultivo']

    # 4. Convertimos textos a números (Encoding)
    print(" Transformando variables de texto a numéricas...")
    X_encoded = pd.get_dummies(X, columns=['dpto', 'prov', 'dist'])

    # 5. Dividimos la data: 80% para entrenar, 20% para examinar al modelo
    print(" Dividiendo la data (Train/Test Split)...")
    X_train, X_test, y_train, y_test = train_test_split(X_encoded, y, test_size=0.2, random_state=42)

    # 6. ¡Llegó la hora de entrenar!
    print(" Entrenando el modelo Random Forest (esto puede tomar unos segunditos)...")
    modelo_rf = RandomForestClassifier(n_estimators=100, random_state=42)
    modelo_rf.fit(X_train, y_train)

    # 7. Evaluamos qué tan bien aprendió
    precision = modelo_rf.score(X_test, y_test)
    print(f" Precisión del modelo en pruebas: {precision * 100:.2f}%")

    # 8. Guardamos el modelo en su "tupperware"
    print(" Guardando el modelo y la estructura de columnas...")
    
    # Creamos la carpeta app/models si no existe
    os.makedirs(os.path.dirname(ruta_modelo), exist_ok=True)
    
    joblib.dump(modelo_rf, ruta_modelo)
    
    # IMPORTANTE: Guardamos también las columnas de X_encoded. 
    # La API necesitará saber el orden exacto de las columnas cuando el agricultor consulte.
    joblib.dump(X_encoded.columns, ruta_columnas)

    print(" ¡Éxito total! Tu modelo está listo y guardado en app/models/")

except FileNotFoundError:
    print(f"¡Oops! No encontré el archivo en la ruta: {ruta_csv}")