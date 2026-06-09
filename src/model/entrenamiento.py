from sklearn.pipeline import Pipeline
from sklearn.model_selection import GridSearchCV

from sklearn.ensemble import RandomForestRegressor

def entrenar_random_forest(X_traim, y_train, preprocessor):

    '''
    Configura y entrena un modelo Random Forest usando validación cruzada
    y grid search

    Args:
        X_train : features de entrenamiento
        y_train : variable objetivo de entrenamiento
        preprocessor : objeto de preprocesamiento

    Returns:
        grid_search : grid_search ya entrenado (para obtener el mejor modelo
                        ,sus mejores parámetros y puntajes) 
    '''
    pipeline = Pipeline([
        ("preprocessor", preprocessor),
        ("model", RandomForestRegressor(random_state=42))
    ])

    param_grid = {
        "model_n_estimators": [100, 200, 300],
        "model_max_depth" : [10, 20, 30, None],
        "model_min_samples_split" : [2, 5, 10],
        "model_min_samples_leaf" : [1, 2, 4]
    }

    grid_search = GridSearchCV(
        estimator=pipeline,
        param_grid=param_grid,
        cv=5,
        scoring="r2",
        n_jobs=-1,
        verbose=2
    )

    grid_search.fit(
        X_train,
        y_train
    )

    return grid_search