from persistencia import cargar_modelo
import pandas as pd
import numpy as np

modelo = cargar_modelo("models/modelo_incidencia_delictiva.joblib")

# Preparación de los datos de entrada
# Las features deben coincidir con las usadas en el entrenamiento:
# - Categóricas: entidad, bien_juridico_afectado, tipo_delito, subtipo_delito, modalidad
# - Numéricas: anio, mes, trimestre

datos_ejemplo = pd.DataFrame(
    {
        "entidad": ["Ciudad de México", "Jalisco"],
        "bien_juridico_afectado": ["El patrimonio", "La vida y la Integridad corporal"],
        "tipo_delito": ["Robo", "Homicidio"],
        "subtipo_delito": ["Robo de vehiculo automotor", "Homicidio doloso"],
        "modalidad": ["Robo de coche de 4 ruedas Con violencia", "Con arma de fuego"],
        "anio": [2026, 2026],
        "mes": [5, 5],
        "trimestre": [1, 1],
    }
)


# El modelo predice en escala logarítmica (log1p), por lo que debemos invertir la transformación
predicciones_log = modelo.predict(datos_ejemplo)
predicciones = np.expm1(predicciones_log)  # Inversión de log1p

resultados = datos_ejemplo.copy()
resultados["incidencia_predicha"] = predicciones.round(0).astype(int)

print("Predicciones de incidencia delictiva:")
print(resultados.to_string(index=False))
