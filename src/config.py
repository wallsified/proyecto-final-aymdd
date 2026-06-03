"""Constantes y configuración global del proyecto.

Centraliza rutas, semillas aleatorias y parámetros de estilo para que
todas las clases y módulos los consuman desde un único punto.
"""

from __future__ import annotations

from pathlib import Path

# Semilla aleatoria global
SEED: int = 42

# Rutas del proyecto.
# ``PROJECT_ROOT`` apunta a la raíz del repositorio (donde vive
# ``pyproject.toml``). Todas las rutas del proyecto se derivan de aquí
# para evitar hardcodes dispersos.
PROJECT_ROOT: Path = Path(__file__).resolve().parents[1]
DATA_DIR: Path = PROJECT_ROOT / "data"
PROCESSED_DIR: Path = DATA_DIR / "processed"
REPORTS_DIR: Path = PROJECT_ROOT / "reports"
FIGURES_DIR: Path = REPORTS_DIR / "figures"
TABLES_DIR: Path = REPORTS_DIR / "tables"

# Dataset principal (única fuente por ahora).
DATASET_CSV: Path = DATA_DIR / "INM_estatal_dic25.csv"
# Salida del pipeline de preprocesamiento.
PROCESSED_CSV: Path = PROCESSED_DIR / "INM_estatal_dic25_clean.csv"

# Metadatos de la fuente de datos.
# Se centralizan aquí para que ``DataRepository`` los reporte en el
# punto 1 del EDA ("fuente y fecha de extracción").
DATA_SOURCE: str = (
    "Secretariado Ejecutivo del Sistema Nacional de Seguridad Pública "
    "(SESNP), mediante datos.gob.mx"
)
DATA_TITLE: str = "Incidencia Delictiva Estatal"
DATA_EXTRACTION_DATE: str = "2026-06-01"
DATA_URL = "https://www.datos.gob.mx/dataset/incidencia_delictiva/resource/d9b2792a-33a2-4ea8-8527-210d9e99de5e"
DATA_ENCODING: str = "utf-8"

# Estilo por defecto de las visualizaciones.
PLOT_DPI: int = 120
PLOT_FIGSIZE: tuple[int, int] = (10, 6)
PLOT_PALETTE: str = "viridis"
SEABORN_THEME: str = "whitegrid"

# Aseguramos que las carpetas de salida existan desde el primer import.
PROCESSED_DIR.mkdir(parents=True, exist_ok=True)
