# Proyecto Final - Minería de Datos Aplicada a México

Proyecto final de la materia Almacenes y Minería de Datos Aplicada a México,
impartida en la Facultad de Ciencias de la UNAM durante el semestre 2026-2.

| Alumnos                     | No. de Cuenta |
| --------------------------- | ------------- |
| Méndez Ávila Luis Geovanni  | 317143980     |
| Paredes Zamudio Luis Daniel | 318159926     |
| Sánchez Rosas Roberto Samuel | 318355159    |

## Dataset a utilizar
El dataset seleccionado para este proyecto es el de Incidencia Delictiva en México, que contiene información detallada sobre los delitos reportados en el país, incluyendo tipos de delitos, ubicaciones geográficas, fechas y otras variables relevantes. Este dataset es proporcionado por el gobierno mexicano a través del portal de datos abiertos y se puede
[descargar aquí](https://www.datos.gob.mx/dataset/incidencia_delictiva/resource/d9b2792a-33a2-4ea8-8527-210d9e99de5e)

## Pasos de ejecución

Se usa `uv` para ejecutar y gestionar el proyecto. La manera más sencilla de correr el proyecto es con el comando:

```bash
uv sync
source .venv/bin/activate
uv run --with jupyter jupyter lab
```

Esto instalará las dependencias, activará el entorno virtual y abrirá Jupyter Lab para que la exploración del proyecto. Una vez dentro del cuaderno se debe seleccionar el kernel del entorno virtual creado por `uv` para que el código se ejecute correctamente, que en este caso se llama `proyecto-final-aymdd`.

## Estructura del proyecto
- `data/`: Carpeta para almacenar los datos utilizados en el proyecto.
- `src/`: Código fuente del proyecto, organizado en módulos y clases.
  - `data/`: Clases y funciones para la carga del conjunto de datos.
  - `eda/`: Clases y funciones para el análisis exploratorio de datos.
- `notebooks/`: Cuadernos de Jupyter para análisis exploratorio, modelado y visualización.
- `requirements.txt`: Archivo con las dependencias del proyecto.
- `styles/`: Carpeta para almacenar estilos CSS personalizados para Quarto.
- `docs/`: Carpeta de despliegue final de los archivos reenderizados con Quarto.
- `report/`: Carpeta para almacenar el reporte final del proyecto en formato PDF y LaTeX.
- `images/`: Carpeta para almacenar imágenes utilizadas en el reporte o documentación.
- `data/`: Carpeta para almacenar los datos utilizados en el proyecto. Por default, viene
vacia, pero aquí es donde debe ser almacenado el dataset a utilizar para el proyecto.