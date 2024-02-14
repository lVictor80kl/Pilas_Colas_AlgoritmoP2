from consola import Consola
from json import load

try:
    # Cargar la configuración desde el archivo JSON
    with open('config.json', 'r') as archivo_json:
        configuracion_cargada = load(archivo_json)

    consola = Consola("C:", configuracion_cargada)  # Unidad por defecto
except Exception as e:
    print("Ocurrio un error al cargar la configuración.")
    print(f"Error: {e}")