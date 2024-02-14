import json


class Archivo:
    def __init__(self, nombre: str, contenido: str, fecha_hora: str):
        """
        Constructor de la clase Archivo.

        Parámetros:
        - nombre (str): El nombre del archivo.
        - contenido (str): El contenido del archivo.
        - fecha_hora (str): La fecha y hora (creación o modificación)
        """
        self.nombre = nombre
        self.contenido = contenido
        self.fecha_hora = fecha_hora

    def to_dict(self) -> dict:
        """
        Convierte el archivo a un diccionario.

        Retorna:
        - dict: El archivo convertido a un diccionario.
        """
        return {'nombre': self.nombre, 'contenido': self.contenido, 'fecha_hora': self.fecha_hora}

    @classmethod
    def from_dict(cls, data: dict):
        """
        Crea una instancia de Archivo a partir de un diccionario.

        Parámetros:
        - data (dict): El diccionario que contiene los datos del archivo.

        Retorna:
        - Archivo: Una nueva instancia de Archivo creada a partir del diccionario.
        """
        return cls(data['nombre'], data['contenido'], data['fecha_hora'])

    def guardar_json(self, filename: str) -> None:
        """
        Guarda el archivo en formato JSON.

        Parámetros:
        - filename (str): El nombre del archivo JSON donde se va a guardar el archivo.

        Retorna:
        - None
        """
        with open(filename, 'w') as f:
            json.dump(self.to_dict(), f, indent=4)

    @classmethod
    def cargar_json(cls, filename: str):
        """
        Carga un archivo desde un archivo JSON.

        Parámetros:
        - filename (str): El nombre del archivo JSON desde donde se va a cargar el archivo.

        Retorna:
        - Archivo: Una nueva instancia de Archivo cargada desde el archivo JSON.
        """
        with open(filename) as f:
            data = json.load(f)
        return cls.from_dict(data)
