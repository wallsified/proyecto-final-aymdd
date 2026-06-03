"""
- Media, mediana, desviación estándar, cuartiles y rango para variables numéricas.
- Frecuencias y moda para variables categóricas.
"""

from __future__ import annotations

from typing import Sequence

import pandas as pd


class StatisticsAnalyzer:
    """Calcula estadísticas e interpreta variables.

    Parameters
    ----------
    df:
        DataFrame a analizar.
    numeric_columns:
        Columnas numéricas.
    categorical_columns:
        Columnas categóricas/texto.
    Nota: Si no se especifican las anteriores, se detectan automáticamente por tipo de dato.
    """

    def __init__(
        self,
        df: pd.DataFrame,
        numeric_columns: Sequence[str] | None = None,
        categorical_columns: Sequence[str] | None = None,
    ) -> None:
        self._df = df
        self._numeric: list[str] = (
            list(numeric_columns)
            if numeric_columns is not None
            else list(df.select_dtypes(include="number").columns)
        )
        self._categorical: list[str] = (
            list(categorical_columns)
            if categorical_columns is not None
            else list(
                df.select_dtypes(include=["category", "object", "string"]).columns
            )
        )

    def numeric_stats(self) -> pd.DataFrame:
        """Resumen descriptivo por columna numérica.

        Returns
        -------
        pd.DataFrame
            Una fila por columna con: promedio, mediana, desviación
            estándar, valor mínimo, Q1, Q3, valor máximo y rango.
        """
        rows: list[dict[str, float | int | str]] = []
        for col in self._numeric:
            s = self._df[col].dropna()
            if s.empty:
                continue
            q1 = float(s.quantile(0.25))
            q3 = float(s.quantile(0.75))
            rows.append(
                {
                    "columna": col,
                    "Promedio": float(s.mean()),
                    "Mediana": float(s.median()),
                    "Desviacíon Estándar": float(s.std()),
                    "Valor Mínimo": float(s.min()),
                    "Q1": q1,
                    "Q3": q3,
                    "Valor Máximo": float(s.max()),
                    # si esta detectando este valor?
                    "range": float(s.max() - s.min()),
                }
            )
        return pd.DataFrame(rows)

    def categorical_stats(self) -> pd.DataFrame:
        """Resumen descriptivo por columna categórica (Punto 3).

        Returns
        -------
        pd.DataFrame
            Una fila por columna con valores únicos, moda y frecuencia modal.
        """
        rows: list[dict[str, float | int | str]] = []
        for col in self._categorical:
            s = self._df[col].dropna()
            if s.empty:
                continue
            counts = s.value_counts()
            mode_label = str(counts.idxmax())
            mode_freq = int(counts.iloc[0])
            rows.append(
                {
                    "columna": col,
                    "valores únicos": int(
                        s.nunique()
                    ),  # number unique, no "not unique"
                    "moda": mode_label,
                    "frecuencia modal": mode_freq,
                }
            )
        return pd.DataFrame(rows)

    def frequency_table(
        self,
        column: str,
        normalize: bool = False,
        top_k: int | None = None,
    ) -> pd.DataFrame:
        """Tabla de frecuencias (absolutas o relativas) de una columna.

        Parameters
        ----------
        column:
            Nombre de la columna.
        normalize:
            Si es verdadero, devuelve proporciones en vez de conteos.
        top_k:
            Si se especifica, devuelve solo las K categorías más frecuentes.
        """
        counts = self._df[column].value_counts(dropna=False, normalize=normalize)
        if top_k is not None:
            counts = counts.head(top_k)
        df = counts.rename("count" if not normalize else "proportion").reset_index()
        df.columns = [column, "count" if not normalize else "proportion"]
        return df


__all__ = ["StatisticsAnalyzer"]
