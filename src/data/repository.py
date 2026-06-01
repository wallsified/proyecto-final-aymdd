"""Repositorio de datos (patrón *Repository*).

``DataRepository`` es la única clase autorizada a leer el CSV. Expone
un ``pandas.DataFrame`` validado contra ``DatasetSchema`` y un objeto
``DatasetMetadata`` con la información de la fuente.
"""

from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path

import pandas as pd

from src import config
from src.data.schema import DatasetSchema


@dataclass(frozen=True)
class DatasetMetadata:
    """Metadatos inmutables de la fuente de datos.

    Attributes
    ----------
    source:
        Nombre de la fuente / publicación.
    title:
        Título del dataset o publicación.
    url:
        URL de la fuente o publicación.
    extraction_date:
        Fecha de extracción o corte de los datos (ISO-8601).

    path:
        Ruta absoluta al CSV.
    """

    source: str
    title: str
    extraction_date: str
    path: Path
    url: str
    encoding: str

    def to_dict(self) -> dict[str, str | int]:
        return {
            "source": self.source,
            "title": self.title,
            "extraction_date": self.extraction_date,
            "path": str(self.path),
            "url": self.url,
            "encoding": self.encoding,
        }


class DataRepository:
    """Carga y valida el dataset de incidencia delictiva.

    Parameters
    ----------
    path:
        Ruta al CSV. Por defecto usa ``config.DATASET_CSV``.
    schema:
        Esquema a aplicar. Por defecto ``DatasetSchema()``.
    metadata:
        Metadatos de la fuente. Si se omite, se construyen desde
        ``scripts.config``.

    Notes
    -----
    La carga es *lazy*: el archivo no se lee hasta llamar a
    :meth:`load`. Esto facilita tests y composición.
    """

    def __init__(
        self,
        path: Path | None = None,
        schema: DatasetSchema | None = None,
        metadata: DatasetMetadata | None = None,
    ) -> None:
        self._path: Path = Path(path) if path is not None else config.DATASET_CSV
        self._schema: DatasetSchema = schema or DatasetSchema()
        self._metadata: DatasetMetadata = metadata or DatasetMetadata(
            source=config.DATA_SOURCE,
            extraction_date=config.DATA_EXTRACTION_DATE,
            title=config.DATA_TITLE,
            url=config.DATA_URL,
            path=self._path,
            encoding=config.DATA_ENCODING,
        )
        self._df: pd.DataFrame | None = None

    @property
    def metadata(self) -> DatasetMetadata:
        return self._metadata

    @property
    def schema(self) -> DatasetSchema:
        return self._schema

    @property
    def df(self) -> pd.DataFrame:
        if self._df is None:
            raise RuntimeError(
                "El DataFrame aún no se ha cargado. Llama a `load()` primero."
            )
        return self._df

    def load(self) -> pd.DataFrame:
        """Lee el CSV, valida columnas y aplica dtypes.

        Returns
        -------
        pd.DataFrame
            DataFrame validado y tipado.
        """
        if not self._path.exists():
            raise FileNotFoundError(
                f"No se encontró el dataset en {self._path}. "
                f"Verifica que el archivo exista y que la ruta sea correcta."
            )

        df = pd.read_csv(
            self._path,
            dtype={k: v for k, v in self._schema.columns.items() if k != "fecha"},
            parse_dates=list(self._schema.parse_dates),
            encoding=self._metadata.encoding,
        )

        self._validate_columns(df)
        self._df = df
        return df

    def _validate_columns(self, df: pd.DataFrame) -> None:
        expected = set(self._schema.expected_columns)
        actual = set(df.columns)
        missing = expected - actual
        unexpected = actual - expected
        if missing or unexpected:
            raise ValueError(
                f"Columnas inconsistentes con DatasetSchema. "
                f"Faltantes={sorted(missing)}, inesperadas={sorted(unexpected)}."
            )
