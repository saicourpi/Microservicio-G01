class MotorAlertas:
    def __init__(self):
        print("🚨 Inicializando el Motor de Alertas Agroclimáticas...")

    def evaluar_clima(self, temp_max: float, temp_min: float, precipitacion: float, humedad: float):
        alertas = []

        # Reglas de Estrés por Calor
        if temp_max > 32:
            alertas.append({
                "tipo": "ESTRÉS TÉRMICO (CALOR)",
                "nivel": "🔴 ROJO",
                "mensaje": f"Temperatura máxima extrema ({temp_max}°C). Alto riesgo de quemaduras en el cultivo y evaporación rápida."
            })
        elif temp_max > 28:
            alertas.append({
                "tipo": "PRECAUCIÓN (CALOR)",
                "nivel": "🟡 AMARILLO",
                "mensaje": f"Temperatura máxima alta ({temp_max}°C). Monitorear la hidratación de las plantas constantemente."
            })

        # ❄️ Reglas de Estrés por Frío
        if temp_min < 10:
            alertas.append({
                "tipo": "ESTRÉS TÉRMICO (FRÍO/HELADA)",
                "nivel": "🔴 ROJO",
                "mensaje": f"Temperatura mínima muy baja ({temp_min}°C). Peligro de heladas y detención del crecimiento."
            })

        # 💧 Reglas de Estrés Hídrico y Biológico
        if humedad < 60 and precipitacion < 5:
            alertas.append({
                "tipo": "ESTRÉS HÍDRICO (SEQUÍA)",
                "nivel": "🔴 ROJO",
                "mensaje": f"Humedad baja ({humedad}%) y escasez de lluvia. Se requiere sistema de riego suplementario urgente."
            })
        elif humedad > 80:
            alertas.append({
                "tipo": "RIESGO BIOLÓGICO (HONGOS)",
                "nivel": "🟡 AMARILLO",
                "mensaje": f"Humedad muy alta ({humedad}%). Condiciones ideales para la proliferación de hongos y plagas."
            })

        # si todo está perfecto
        if len(alertas) == 0:
            alertas.append({
                "tipo": "CLIMA ÓPTIMO",
                "nivel": "🟢 VERDE",
                "mensaje": "Las condiciones climáticas históricas son estables y favorables para la siembra."
            })

        return alertas

# Instanciamos el motor para usarlo en nuestras rutas
motor_alertas = MotorAlertas()