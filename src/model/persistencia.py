import jolib

def guardar_modelo(modelo, nombre_archivo):
    '''
    Guarda el modelo en un archivo usando joblib

    Args:
        modelo : el modelo entrenado
        nombre_archivo :  Ruta completa o nombre del archivo donde se guardará
    '''
    jolib.dump(modelo, nombre_archivo)
    print(f"Modelo guardado en {nombre_archivo}")

def cargar_modelo(nombre_archivo):
    '''
    Carga el modelo previamente guardado con joblib

    Args:
        nombre_archivo : Ruta completa o nombre del archivo a cargar

    Returns:
        modelo : el modelo listo para ser usado
    '''
    modelo = jolib.load(nombre_archivo)
    print(f"Modelo cargado desde: {nombre_archivo}")
    return modelo