# Proyecto Final - Minería de Datos Aplicada a México

Proyecto final de la materia Almacenes y Minería de Datos Aplicada a México,
impartida en la Facultad de Ciencias de la UNAM durante el semestre 2026-2.

| Alumnos                     | No. de Cuenta |
| --------------------------- | ------------- |
| Méndez Ávila Luis Geovanni  | 317143980     |
| Paredes Zamudio Luis Daniel | 318159926     |
| Sánchez Rosas Roberto Samuel | 318355159    |


## Resumen

Este repositorio contiene el análisis y modelado sobre el conjunto de datos
"Incidencia Delictiva en México" (2015–2025). El objetivo del proyecto es
realizar un análisis exploratorio, construir modelos predictivos y un análisis
de clustering a nivel estatal.

## Dataset

El dataset original es público y proviene del Secretariado Ejecutivo del Sistema
Nacional de Seguridad Pública (SESNSP). Se puede descargar desde [este enlace](
https://www.datos.gob.mx/dataset/incidencia_delictiva/resource/d9b2792a-33a2-4ea8-8527-210d9e99de5e)

En este repositorio los datos se encuentran (si se han descargado o procesado):

- `data/INM_estatal_dic25.csv` — CSV original
- `data/processed/INM_estatal_dic25_clean.csv` — CSV procesado por el pipeline de preprocesamiento (limpieza, transformación, etc.)
- `data/processed/entidades_segmentadas.csv` — resultados del clustering

## Requisitos

- Python >= 3.11
- Quarto (opcional para renderizar la documentación y generar PDF)
- La gestión de dependencias se realiza desde `pyproject.toml` y el lock-file
  `uv.lock`.

Se recomienda usar la herramienta `uv` incluida en el flujo de trabajo del
proyecto (ver sección siguiente).

## Instalación y ejecución

Recomendado (flujo reproducible con `uv`)

1. Desde la raíz del proyecto ejecute:

```bash
uv sync
```

Esto crea/actualiza el entorno virtual y sincroniza las dependencias según
`uv.lock`.

2. Active el entorno virtual:

- macOS / Linux:

```bash
source .venv/bin/activate
```

- Windows (PowerShell):

```powershell
.\.venv\Scripts\Activate.ps1
```

3. Ejecutar Jupyter Lab (dentro del entorno):

```bash
uv run --with jupyter jupyter lab
```

Desde aqui se abre el cuaderno ha ejecutar desde Jupyter Lab. Se selecciona el kernel
correspondiente al entorno virtual generado (en el repositorio el kernel se
identifica típicamente como `proyecto-final-aymdd`; si no aparece, se selecciona el
kernel de Python asociado a `.venv`).


## Estructura del proyecto

- `data/` — datos crudos y procesados
  - `processed/` (salidas del pipeline)
- `notebooks/` — Jupyter notebooks (EDA, modelado, clustering)
- `src/` — código fuente del proyecto (módulos de carga de datos, EDA,
  preprocesamiento, modelado y clustering)
- `reports/` — archivos LaTeX y recursos para el reporte (bibliografía, imágenes)
- `presentation/` — archivos y recursos para la presentación (Quarto)
- `styles/` — estilos personalizados para Quarto
- `docs/` — sitio y PDF generados por Quarto (salida)
- `_quarto.yml` — configuración del sitio Quarto
- `pyproject.toml`, `uv.lock` — metadatos y dependencias del proyecto

## Sitio web y PDF
- El sitio web generado por Quarto se encuentra en `docs/` y se puede abrir el
  archivo `index.html` para navegarlo localmente. Pero también se puede abrir desde
  GitHub Pages en la URL: (https://wallsified.github.io/proyecto-final-aymdd/)
- El PDF del reporte se encuentra en `reports/Análisis-de-Incidencia-Delictiva-en-México-2015-2025.pdf` y también se puede leer y descargar desde el sitio web haciendo clic en el enlace correspondiente.
- La presentación en formato Quarto se encuentra en `presentation/` y se puede abrir el archivo `presentation.html` en algún
navegador para visualizarla. También se puede acceder a ella desde el sitio web en el enlace correspondiente.