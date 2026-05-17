# Microservicio G01 - Predicción de Rendimiento Agrícola

Este repositorio contiene el microservicio backend encargado de predecir el rendimiento agrícola utilizando modelos de Machine Learning. La API procesa variables climáticas para generar estimaciones producción.

## Estado del Proyecto
En fase inicial (Configuración del entorno y estructuración de la API).

## Stack Tecnológico
* **Framework:** FastAPI
* **Procesamiento de Datos:** Pandas / NumPy
* **Machine Learning:** Scikit-learn
* **Servidor:** Uvicorn

## Estructura del Microservicio
Próximamente se integrarán los siguientes componentes:
* `main.py`: Punto de entrada de la API y definición de las rutas (endpoints).
* `models/`: Carpeta que contendrá los modelos predictivos ya entrenados (archivos `.pkl` o `.joblib`).
* `data/`: Datasets de prueba sobre clima y agricultura.

## Endpoints Principales
* `GET /`: Verificación del estado del servidor.
* `POST /predict`: Recibe los datos climáticos en formato JSON y devuelve la predicción del rendimiento.

## Autores:
* Lesly Cusichi
* Jair Salvador
* Jean Franco Cruzado
* Jesus Pacahuala