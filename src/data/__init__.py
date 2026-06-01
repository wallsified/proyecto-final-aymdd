"""Capa de datos: ``DataRepository`` y ``DatasetSchema``.

Aísla la lectura del CSV detrás de una interfaz uniforme (patrón
*Repository*) para que el EDA y futuros módulos de modelado no se
acoplen al origen físico de los datos.
"""

from src.data.repository import DataRepository, DatasetMetadata
from src.data.schema import DatasetSchema

__all__ = ["DataRepository", "DatasetMetadata", "DatasetSchema"]
