"""Preprocesamiento simple del dataset de incidencia delictiva.

Pipeline mínimo con cuatro pasos en orden:

1. drop_columns: elimina las columnas declaradas por el usuario.
2. fecha (en texto) → datetime.
3. Elimina filas con nulos en columnas críticas.
4. Elimina duplicados exactos.

Cada paso imprime en pantalla un resumen para que la transformación
del dataset sea visible, en línea con el estilo del proyecto.
"""

from __future__ import annotations

from pathlib import Path

import pandas as pd

from src.config import PROCESSED_CSV, DATA_ENCODING

# Columnas en las que un NaN implica eliminar la fila completa.
# Por defecto: la métrica objetivo, la fecha y la entidad.
DEFAULT_CRITICAL_COLS: tuple[str, ...] = (
    "incidencia_delictiva",
    "fecha",
    "entidad",
)


class PreprocessingPipeline:
    """Pipeline simple de preprocesamiento.

    Parameters
    ----------
    drop_columns:
        Columnas a eliminar antes del resto de operaciones. Las que
        no existan en el DataFrame se ignoran con un aviso.
    critical_cols:
        Columnas en las que un NaN implica eliminar la fila.
        Default: :data:DEFAULT_CRITICAL_COLS.
    drop_nulls:
        Si es True, elimina filas con nulos en critical_cols.
    drop_duplicates:
        Si es True, elimina filas duplicadas exactas.
    date_col:
        Columna a convertir a datetime
    output_path:
        Ruta del CSV de salida. Default: config.PROCESSED_CSV.
    encoding:
        Codificación del CSV de salida. Default: config.DATA_ENCODING
    """

    def __init__(
        self,
        drop_columns: list[str] | None = None,
        critical_cols: tuple[str, ...] = DEFAULT_CRITICAL_COLS,
        date_col: str = "fecha",
        output_path: Path | None = None,
        encoding: str = DATA_ENCODING,
    ) -> None:
        self._drop_columns: list[str] = list(drop_columns or [])
        self._critical_cols: tuple[str, ...] = tuple(critical_cols)
        self._date_col = date_col
        self._output_path: Path = (
            Path(output_path) if output_path is not None else PROCESSED_CSV
        )
        self._encoding = encoding

    @property
    def drop_columns(self) -> list[str]:
        return list(self._drop_columns)

    @property
    def output_path(self) -> Path:
        return self._output_path

    def run(self, df: pd.DataFrame) -> pd.DataFrame:
        """Aplica los pasos del pipeline y devuelve el DataFrame limpio.

        Returns
        -------
        pd.DataFrame
            Copia limpia del DataFrame original.
        """

        working = df.copy()
        working = self._step_drop_columns(working)
        working = self._step_convert_dates(working)
        working = self._step_drop_nulls(working)
        working = self._step_drop_duplicates(working)

        if "entidad" in working.columns:
            print("[5] Normalizando nombres de entidades federativas")
            working["entidad"] = working["entidad"].replace(
                {
                    "Veracruz de Ignacio de la Llave": "Veracruz",
                    "Coahuila de Zaragoza": "Coahuila",
                    "Michoacán de Ocampo": "Michoacán",
                }
            )

        return working

    def save(self, df: pd.DataFrame) -> None:
        """Persiste df en output_path como CSV."""
        self._output_path.parent.mkdir(parents=True, exist_ok=True)
        df.to_csv(self._output_path, index=False, encoding=self._encoding)
        print(
            f"CSV limpio guardado en:\n {self._output_path}\n"
            f"{len(df):,} filas x {df.shape[1]} columnas, "
        )

    def _step_drop_columns(self, df: pd.DataFrame) -> pd.DataFrame:
        print("[1] Eliminando columnas declaradas en drop_columns")
        if not self._drop_columns:
            print("(ninguna columna configurada)")
            return df

        existing = [c for c in self._drop_columns if c in df.columns]
        missing = [c for c in self._drop_columns if c not in df.columns]
        if existing:
            df = df.drop(columns=existing)
        print(f" Eliminadas: {existing or 'ninguna'}")
        if missing:
            print(f" No encontradas (ignoradas): {missing}")
        return df

    def _step_convert_dates(self, df: pd.DataFrame) -> pd.DataFrame:
        print("[2] Convirtiendo '{self._date_col}' a datetime")

        if self._date_col not in df.columns:
            raise KeyError(f"Falta la columna de fecha: {self._date_col!r}.")
        parsed = pd.to_datetime(df[self._date_col], errors="coerce")
        n_ok = int(parsed.notna().sum())
        n_failed = int(parsed.isna().sum())
        df[self._date_col] = parsed
        print(f"   OK={n_ok:,} / fallidos={n_failed:,}")
        if n_ok:
            print(f" Rango: {parsed.min().date()} → {parsed.max().date()}")

        return df

    def _step_drop_nulls(self, df: pd.DataFrame) -> pd.DataFrame:
        print("[3] Eliminando filas con nulos en críticas")
        critical = [c for c in self._critical_cols if c in df.columns]
        before = len(df)
        df = df.dropna(subset=critical).reset_index(drop=True)
        print(f"Filas: {before:,} -> {len(df):,} (eliminadas: {before - len(df):,})")
        return df

    def _step_drop_duplicates(self, df: pd.DataFrame) -> pd.DataFrame:
        print("[4] Eliminando duplicados exactos")
        before = len(df)
        df = df.drop_duplicates().reset_index(drop=True)
        print(f"Filas: {before:,} -> {len(df):,} (eliminadas: {before - len(df):,})")
        return df


__all__ = ["PreprocessingPipeline"]
