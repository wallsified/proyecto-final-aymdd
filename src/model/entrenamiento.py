from sklearn.pipeline import Pipeline
from sklearn.model_selection import RandomizedSearchCV

from sklearn.ensemble import RandomForestRegressor


def entrenar_random_forest(X_train, y_train, preprocessor):
    """
    Configura y entrena un modelo Random Forest usando validación cruzada
    y búsqueda aleatoria de hiperparámetros usando RandomizedSearchCV para
    optimizar el rendimiento del modelo.

    Args:
        X_train : features de entrenamiento
        y_train : variable objetivo de entrenamiento
        preprocessor : objeto de preprocesamiento

    Returns:
        search : RandomizedSearchCV ya entrenado (para obtener el mejor modelo,
                 sus mejores parámetros y puntajes)
    """
    pipeline = Pipeline(
        [
            ("preprocessor", preprocessor),
            ("model", RandomForestRegressor(random_state=42)),
        ]
    )

    param_distributions = {
        "model__n_estimators": [100, 150],
        "model__max_depth": [15, None],
        "model__min_samples_split": [2, 5],
    }

    search = RandomizedSearchCV(
        estimator=pipeline,
        param_distributions=param_distributions,
        n_iter=8,
        cv=3,
        scoring="r2",
        n_jobs=-1,
        random_state=42,
        verbose=1,
    )

    search.fit(X_train, y_train)

    return search
