"""Módulo de Análisis Exploratorio de Datos (EDA).

Reúne las clases que cubren los puntos de la rúbrica del EDA.
"""

from src.eda.outliers import OutlierDetector
from src.eda.statistics import StatisticsAnalyzer

__all__ = [
    "OutlierDetector",
    "StatisticsAnalyzer",
]
