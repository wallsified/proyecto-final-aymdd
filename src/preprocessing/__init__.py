"""Capa de preprocesamiento: pipeline simple de limpieza.

Consolida en una sola clase :class:`PreprocessingPipeline` los pasos
necesarios para dejar el dataset listo para análisis/modelado:

* ``drop_columns``: eliminar columnas declaradas por el usuario.
* Conversión de ``fecha`` a ``datetime``.
* Eliminación de filas con nulos en columnas críticas.
* Eliminación de duplicados exactos.
"""

from src.preprocessing.preprocessing import (
    DEFAULT_CRITICAL_COLS,
    PreprocessingPipeline,
)

__all__ = ["DEFAULT_CRITICAL_COLS", "PreprocessingPipeline"]
