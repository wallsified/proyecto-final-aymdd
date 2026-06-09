import pandas as pd
import numpy as np

from sklearn.compose import ColumnTransformer
from sklearn.preprocessing import(OneHotEncoder, StandardScaler)

def cargar_preparar_datos(ruta):
    '''
    Carga un archivo csv que contiene los datos del proyecto

    Args:
        ruta : la ruta del archivo CSV a cargar
    '''
    df = pd.read_csv(ruta)

    return df

def separar_features_target(df):
    '''
    Separa el dataframe en el conjunto de features (variables que no son la objetivo)
    y la variable objetivo.

    Aplica una transformación logaritmica para tratar el desvalance observado en el EDA
    de la variable objetivo

    Args:
        df : el dataframe que tiene tanto features como la variable objetivo

    Returns:
        X : el dataframe sin la columna de la variable objetivo
        y : La columna de la variable objetivo (ya con la transformación)
    '''

    target = "incidencia_delictiva"

    y = np.log1p(df[target])
    X = df.drop(columns=[target])

    return X, y

def construir_preprocesador(X):
    categoricas = X.select_dtypes(
        include=["object", "category"]
    ).columns.tolist()

    numericas = X.select_dtypes(
        include=["int64", "float64"]
    ).columns.tolist()

    preprocessor = ColumnTransformer(
        transformers=[
            (
                "cat", OneHotEncoder(
                    handle_unknown="ignore"
                ),
                categoricas
            ),
            (
                "num",
                StandardScaler(),
                numericas
            )
        ]
    )

    return preprocessor