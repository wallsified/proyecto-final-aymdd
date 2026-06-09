import numpy as np
import pandas as pd

from sklearn.metrics import(
    mean_absolute_error,
    mean_squared_error,
    r2_score
)

import matplotlib.pyplot as plt

def evaluar_modelo(modelo, X_test, y_test):
    '''
    Calcula las métricas de rendimiento

    Realiza predicciones sobre el conjunto de prueba y evalua el desempeño
    usando MAE, MSE, RMSE, R2

    Args:
        modelo : Modelo de Random Forest regressor entrenado
        X_test : Features de prueba
        y_test : Valores de la variable objetivo de prueba
    
    Returns:
        metricas : dataframe con los nombre de las métricas y sus valores
        y_pred : las predicciones generadas por el modelo
    '''
    y_pred = model.predict(X_test)

    mae = mean_absolute_error(y_test, y_pred)
    mse = mean_squared_error(y_test, y_pred)
    rmse = np.sqrt(mse)
    r2 = r2_score(y_test, y_pred)

    metricas = pd.DataFrame({
        "Metrica" : ["MAE", "MSE", "RMSE", "R2"],
        "Valor" : [mae, mse, rmse, r2]
    })

    return metricas, y_pred

def grafica_residuales(y_test, y_pred):
    '''
    Genera una gráfica de residuales contra las predicciones

    Args:
        y_test : valores reales de la variable objetivo
        y_pred : valores predichos por el modelo
    '''
    residuals = y_test - y_pred

    plt.figure(figsize=(8,6))

    plt.scatter(y_pred, residuals, alpha=0.3)

    plt.axhline(0, linestyle="--")

    plt.title("Grafica de residuales")

    plt.xlabel("Prediccion")

    plt.ylabel("Residual")

    plt.show()

def grafica_predicciones(y_test, y_pred):
    '''
    Genera una gráfica que compara los valores reales contra los predichos

    Args:
        y_test : valores reales de la variable objetivo
        y_pred : valores predichos por el modelo
    '''


    plt.figure(figsize=(8,6))
    
    plt.scatter(y_test, y_pred, alpha=0.3)

    plt.plot(
        [y_test.min(), y_test.max()],
        [y_test.min(), y_test.max()],
        'r--'
    )

    plt.xlabel("Real")

    plt.ylabel("Predicho")

    plt.title("Real vs Predicho")

    plt.show()