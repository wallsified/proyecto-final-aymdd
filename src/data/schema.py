"""Esquema esperado del CSV de incidencia delictiva.

Define los nombres y tipos de columna canónicos. ``DataRepository``
lo usa para validar la carga y reportar inconsistencias antes del EDA.
"""

from __future__ import annotations
import pandas as pd
from dataclasses import dataclass, field
from typing import Sequence


@dataclass(frozen=True)
class DatasetSchema:
    """Definición inmutable del esquema del dataset.

    Attributes
    ----------
    columns:
        Mapeo ``nombre_columna -> tipo_pandas`` (string entendible por
        ``pd.read_csv(dtype=...)``).
    parse_dates:
        Columnas a parsear como fecha por ``pandas``.
    descriptions:
        Diccionario de datos: mapeo ``nombre_columna -> descripción``
        legible del contenido de la variable.
    """

    # Columnas de origen del dataset. Se "hardcodean" para validar la carga y reportar inconsistencias antes del EDA.
    # y/o para, en caso de algún error, identificar rápidamente qué columnas faltan o están mal nombradas.
    columns: dict[str, str] = field(
        default_factory=lambda: {
            "anio": "int64",
            "clave_ent": "int64",
            "entidad": "string",
            "bien_juridico_afectado": "category",
            "tipo_delito": "category",
            "subtipo_delito": "category",
            "modalidad": "category",
            "mes": "category",
            "fecha": "string",
            "incidencia_delictiva": "int64",
            "entidad_federativa": "string",
        }
    )
    parse_dates: Sequence[str] = ("fecha",)

    # Información copiada textualmente de la fuente original con modificaciones para entender mejor el contenido de cada variable.
    descriptions: dict[str, str] = field(
        default_factory=lambda: {
            "anio": "Año de registro de las averiguaciones previas y/o carpetas de investigación.",
            "clave_ent": "Clave de la entidad, según el Marco Geoestadístico Nacional (MGN) del Instituto Nacional de Geografía y Estadística (INEGI).",
            "entidad": "Entidad federativa de registro de las averiguaciones previas y/o carpetas de investigación.",
            "bien_juridico_afectado": "Primera clasificación de los delitos en las averiguaciones previas y/o carpetas de investigación. (Patrimonio, vida, libertad, etc.)",
            "tipo_delito": "Segunda clasificación de los delitos. (Falsedad, Lesiones, Robo, etc.)",
            "subtipo_delito": "Tercera clasificación de los delitos. Subcategorías específicas de cada tipo de delito. (Lesiones dolosas, etc. Puede ser repetido con la anterior)",
            "modalidad": "Cuarta clasificación de los delitos. Forma en la que se comete el delito. (Con violencia, sin violencia, etc.)",
            "mes": "Mes de registro de las averiguaciones previas y/o carpetas de investigación.",
            "fecha": "Fecha de registro de las averiguaciones previas y/o carpetas de investigación.",
            "incidencia_delictiva": "Incidencia delictiva del Fuero Común (Número absoluto de presuntos delitos registrados)",
            "entidad_federativa": "Entidad federativa de registro de las averiguaciones previas y/o carpetas de investigación.",
        }
    )

    @property
    def expected_columns(self) -> list[str]:
        return list(self.columns.keys())

    def expected_dtypes(self) -> dict[str, str]:
        return dict(self.columns)

    def data_dictionary(self) -> "pd.DataFrame":
        """Devuelve el diccionario de datos como DataFrame.

        Returns
        -------
        pd.DataFrame
            Tabla con columnas ``columna``, ``tipo`` y ``descripcion``.
        """
        import pandas as pd

        pd.set_option("display.max_colwidth", 200)
        return pd.DataFrame(
            [
                {
                    "columna": col,
                    "tipo": dtype,
                    "descripcion": self.descriptions.get(col, ""),
                }
                for col, dtype in self.columns.items()
            ],
        )
