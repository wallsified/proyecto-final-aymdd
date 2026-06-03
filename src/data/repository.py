"""Repositorio de datos

DataRepository es la única clase autorizada a leer un CSV del
proyecto. Expone un pandas.DataFrame y un objeto DatasetMetadata
con la información de la fuente (si es que la hay)

Soporta varios datasets coexistiendo, basta con instanciar el
repositorio una vez por cada uno, pasando su ruta en el constructor.
"""

from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path

import pandas as pd

from src import config
from ..data.dictionary import OriginalDataDictionary

# instancia única del diccionario de datos original, para que el repositorio pueda
# referenciarlo al cargar el dataset original (y también para que los esquemas puedan
# referenciarlo al describir columnas sin tener que repetir la descripción en cada esquema)
ORIGINAL_DATA_DICTIONARY = OriginalDataDictionary()


@dataclass(frozen=True)
class DatasetMetadata:
    """Metadatos originales de la fuente de datos.

    Attributes
    ----------
    source:
        Nombre de la fuente / publicación.
    title:
        Título del dataset o publicación.
    extraction_date:
        Fecha de extracción o corte de los datos (ISO-8601).
    path:
        Ruta absoluta al CSV.
    url:
        URL de la fuente o publicación.
    encoding:
        Codificación del archivo.
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
    """Carga y (opcionalmente) valida un dataset desde un CSV.

    Parameters
    ----------
    path:
        Ruta al CSV. Si se omite, se usa config.DATASET_CSV.1
    metadata:
        Metadatos completos. Si se omite, se construyen a partir de
        config y de los overrides source/title/... (si los hay).
    source, title, extraction_date, url, encoding:
        Overrides convenientes para los metadatos sin tener que armar
        un :class:DatasetMetadata completo.

    Notes
    -----
    La carga es lazy: el archivo no se lee hasta llamar load().
    """

    def __init__(
        self,
        path: str | Path | None = None,
        *,
        metadata: DatasetMetadata | None = None,
        source: str | None = None,
        title: str | None = None,
        extraction_date: str | None = None,
        url: str | None = None,
        encoding: str | None = None,
    ) -> None:
        path_provided = path is not None
        self._path: Path = Path(path) if path_provided else config.DATASET_CSV

        if metadata is not None:
            self._metadata = metadata
        else:
            self._metadata = DatasetMetadata(
                source=source if source is not None else config.DATA_SOURCE,
                title=title if title is not None else config.DATA_TITLE,
                extraction_date=(
                    extraction_date
                    if extraction_date is not None
                    else config.DATA_EXTRACTION_DATE
                ),
                url=url if url is not None else config.DATA_URL,
                encoding=encoding if encoding is not None else config.DATA_ENCODING,
                path=self._path,
            )

        self._df: pd.DataFrame | None = None

    @property
    def metadata(self) -> DatasetMetadata:
        return self._metadata

    @property
    def df(self) -> pd.DataFrame:
        if self._df is None:
            raise RuntimeError(
                "El DataFrame aún no se ha cargado. Utiliza load() primero."
            )
        return self._df

    def load(self) -> pd.DataFrame:
        """Lee el CSV y, si el esquema lo pide, aplica dtypes y validación.

        Returns
        -------
        pd.DataFrame
            DataFrame cargado (validado y tipado si el esquema lo pide).
        """
        if not self._path.exists():
            raise FileNotFoundError(
                f"No se encontró el dataset en {self._path}. "
                f"Verifica que el archivo exista y que la ruta sea correcta."
            )

        read_kwargs: dict = {"encoding": self._metadata.encoding}
        df = pd.read_csv(self._path, **read_kwargs)
        self._df = df
        return df

    def dictionary(self) -> pd.DataFrame:
        """Devuelve el diccionario de datos del dataset original."""
        if self._df is None:
            raise RuntimeError(
                "El DataFrame aún no se ha cargado. Utiliza load() primero."
            )
        return ORIGINAL_DATA_DICTIONARY.data_dictionary(self._df)
