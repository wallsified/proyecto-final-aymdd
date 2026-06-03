"""
El diccionario de datos canónico del dataset original.
Como posteriormente se utilizará una versión limpia/procesada,
este diccionario se mantiene separado del esquema de validación
pero como referencia global para describir las columnas en cualquier versión del dataset.
"""

import pandas as pd
from dataclasses import dataclass

COLUMN_DESCRIPTIONS: dict[str, str] = {
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

COLUMN_DTYPES: dict[str, str] = {
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


@dataclass(frozen=True)
class OriginalDataDictionary:
    """Diccionario de datos canónico del dataset original.

    Este diccionario se mantiene separado del esquema de validación
    pero como referencia global para describir las columnas en cualquier versión del dataset.
    """

    def data_dictionary(self, df: pd.DataFrame) -> pd.DataFrame:
        """Devuelve el diccionario de datos como DataFrame.

        Parameters
        ----------
        df:
            Si se proporciona, las filas describen las columnas y dtypes
            reales del DataFrame. Si se omite, se usan las columnas
            declaradas en columns.

        Returns
        -------
        pd.DataFrame
            Tabla con columnas columna, tipo y descripcion.
        """
        if df is not None:
            cols = list(df.columns)
            dtypes = {c: str(df[c].dtype) for c in cols}
        elif df.columns:
            cols = list(self.columns.keys())
            dtypes = dict(self.columns)
        else:
            raise ValueError(
                "Sin DataFrame ni columns en el esquema: nada que describir. "
            )

        return pd.DataFrame(
            {
                "columna": cols,
                "tipo": [dtypes.get(c, "desconocido") for c in cols],
                "descripcion": [
                    COLUMN_DESCRIPTIONS.get(c, "Sin descripción.") for c in cols
                ],
            }
        )
