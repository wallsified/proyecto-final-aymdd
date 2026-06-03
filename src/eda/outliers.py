"""Detección y tratamiento de valores atípicos."""

from __future__ import annotations

from typing import Sequence

import pandas as pd


class OutlierDetector:
    """Detecta valores atípicos en columnas numéricas y los marca/recorta/elimina.

    Parameters
    ----------
    df:
        DataFrame a analizar.
    columns:
        Columnas numéricas a inspeccionar.
    iqr_multiplier:
        Multiplicador del rango intercuartílico. 1.5 marca outliers
        "moderados" (default); 3.0 marca solo extremos.
    """

    def __init__(
        self,
        df: pd.DataFrame,
        columns: Sequence[str] | None = None,
    ) -> None:
        self._df = df
        self._columns: list[str] = (
            list(columns)
            if columns is not None
            else list(df.select_dtypes(include="number").columns)
        )

    def _bounds_iqr(self, s: pd.Series) -> tuple[float, float]:
        q1 = float(s.quantile(0.25))
        q3 = float(s.quantile(0.75))
        iqr = q3 - q1
        return q1 - 1.5 * iqr, q3 + 1.5 * iqr

    def flag(self, suffix: str = "_is_outlier") -> pd.DataFrame:
        """Devuelve una copia del DataFrame con columnas booleanas
        para indicar si cada valor es un outlier según el método IQR.
        """
        out = self._df.copy()
        for col in self._columns:
            s = out[col]
            lower, upper = self._bounds_iqr(s.dropna())
            out[f"{col}{suffix}"] = (
                ((s < lower) | (s > upper)).fillna(False).astype(bool)
            )
        return out

    def drop(self) -> pd.DataFrame:
        """Elimina filas con outliers en cualquiera de las columnas analizadas.

        Usar con cautela: en incidencia delictiva los extremos suelen ser
        señales reales, no errores. Justifica el uso antes de aplicarlo.
        """
        any_outlier = pd.Series(False, index=self._df.index)
        for col in self._columns:
            s = self._df[col]
            lower, upper = self._bounds_iqr(s.dropna())
            any_outlier |= ((s < lower) | (s > upper)).fillna(False)
        return self._df.loc[~any_outlier].copy()

    def summary(self) -> pd.DataFrame:
        """Resumen combinado: estadísticos básicos + límites + outliers.

        Returns
        -------
        pd.DataFrame
            Una fila por columna con ``n_total``, ``min``,
            ``max``, ``lower``, ``upper``, ``n_outliers`` y ``pct_outliers``.
        """
        rows: list[dict[str, float | int | str]] = []
        for col in self._columns:
            s = self._df[col].dropna()
            if s.empty:
                continue
            lower, upper = self._bounds_iqr(s)
            n_out = int(((s < lower) | (s > upper)).sum())
            rows.append(
                {
                    "columna": col,
                    "n_total": int(len(s)),
                    "min": float(s.min()),
                    "max": float(s.max()),
                    "lower": float(lower),
                    "upper": float(upper),
                    "n_outliers": n_out,
                    "pct_outliers": 100.0 * n_out / len(s),
                }
            )
        return pd.DataFrame(rows)


__all__ = ["OutlierDetector"]
