from nodo import Nodo
from archivo import Archivo
import json
from typing import Optional


class Carpeta:
    def __init__(self, nombre: str, fecha_hora: str):
        """
        Constructor de la clase Carpeta.

        Parámetros:
        - nombre (str): El nombre de la carpeta.
        - fecha_hora (str): La fecha y hora (creación o modificación)
        """
        self.nombre = nombre
        self.fecha_hora = fecha_hora
        self.primer_archivo = None  # Referencia al primer archivo en la lista.
        self.ultimo_archivo = None  # Referencia al último archivo en la lista.

    def crear_archivo(self, nombre: str, contenido: str, fecha_hora: str) -> None:
        """
        Método para crear un nuevo archivo y agregarlo al final de la cola.

        Parámetros:
        - nombre (str): El nombre del archivo.
        - contenido (str): El contenido del archivo.
        - fecha_hora (str): La fecha y hora (creación o modificación)

        Retorna:
        - None
        """
        archivo = Archivo(nombre, contenido, fecha_hora)
        nodo = Nodo(archivo)
        if self.primer_archivo is None:
            self.primer_archivo = nodo
            self.ultimo_archivo = nodo
        else:
            self.ultimo_archivo.siguiente = nodo
            self.ultimo_archivo = nodo

    def buscar_archivo(self, nombre: str) -> Optional['Archivo']:
        """
        Busca un archivo por su nombre dentro de la carpeta actual.

        Parámetros:
        - nombre (str): El nombre del archivo que se está buscando.

        Retorna:
        - Archivo | None: El archivo encontrado si existe, None si no se encuentra.
        """
        # Comenzamos desde el primer archivo en la carpeta
        nodo_actual = self.primer_archivo

        # Iteramos sobre cada archivo en la carpeta
        while nodo_actual:
            # Verificamos si el nodo actual contiene un archivo y si su nombre coincide con el buscado
            if isinstance(nodo_actual.dato, Archivo) and nodo_actual.dato.nombre == nombre:
                return nodo_actual.dato  # Devolvemos el archivo si lo encontramos
            # Avanzamos al siguiente nodo en la lista
            nodo_actual = nodo_actual.siguiente

        # Si no se encontró el archivo, retornamos None
        return None

    def crear_carpeta(self, nombre: str, fecha_hora: str) -> None:
        """
        Método para crear una nueva carpeta y agregarla al final de la cola.

        Parámetros:
        - nombre (str): El nombre de la carpeta.
        - fecha_hora (str): La fecha y hora (creación o modificación)

        Retorna:
        - None
        """
        nueva_carpeta = Carpeta(nombre, fecha_hora)
        nodo = Nodo(nueva_carpeta)
        if self.primer_archivo is None:
            self.primer_archivo = nodo
            self.ultimo_archivo = nodo
        else:
            self.ultimo_archivo.siguiente = nodo
            self.ultimo_archivo = nodo

    def buscar_carpeta(self, nombre: str) -> Optional['Carpeta']:
        """
        Busca una carpeta por su nombre dentro de la carpeta actual de forma recursiva.

        Parámetros:
        - nombre (str): El nombre de la carpeta que se está buscando.

        Retorna:
        - Carpeta | None: La carpeta encontrada si existe, None si no se encuentra.
        """
        # Comenzamos desde el primer archivo en la carpeta
        nodo_actual = self.primer_archivo

        # Iteramos sobre cada archivo en la carpeta
        while nodo_actual:
            # Verificamos si el nodo actual contiene una carpeta y si su nombre coincide con el buscado
            if isinstance(nodo_actual.dato, Carpeta) and nodo_actual.dato.nombre == nombre:
                return nodo_actual.dato  # Devolvemos la carpeta si la encontramos
            # Avanzamos al siguiente nodo en la lista
            nodo_actual = nodo_actual.siguiente

        # Si no se encontró la carpeta, retornamos None
        return None

    def eliminar_archivo(self, nombre: str) -> bool:
        """
        Método para eliminar un archivo de la carpeta.

        Parámetros:
        - nombre (str): El nombre del archivo a eliminar.

        Retorna:
        - bool: True si el archivo fue eliminado exitosamente, False en caso contrario.
        """
        nodo_actual = self.primer_archivo
        nodo_anterior = None
        while nodo_actual:
            if isinstance(nodo_actual.dato, Archivo) and nodo_actual.dato.nombre == nombre:
                if nodo_anterior:
                    nodo_anterior.siguiente = nodo_actual.siguiente
                    if nodo_actual == self.ultimo_archivo:
                        self.ultimo_archivo = nodo_anterior
                else:
                    self.primer_archivo = nodo_actual.siguiente
                    if nodo_actual == self.ultimo_archivo:
                        self.ultimo_archivo = None
                return True
            nodo_anterior = nodo_actual
            nodo_actual = nodo_actual.siguiente
        return False

    def eliminar_carpeta(self, nombre: str) -> bool:
        """
        Método para eliminar una carpeta de la carpeta.

        Parámetros:
        - nombre (str): El nombre de la carpeta a eliminar.

        Retorna:
        - bool: True si la carpeta fue eliminada exitosamente, False en caso contrario.
        """
        nodo_actual = self.primer_archivo
        nodo_anterior = None
        while nodo_actual:
            if isinstance(nodo_actual.dato, Carpeta) and nodo_actual.dato.nombre == nombre:
                if nodo_anterior:
                    nodo_anterior.siguiente = nodo_actual.siguiente
                    if nodo_actual == self.ultimo_archivo:
                        self.ultimo_archivo = nodo_anterior
                else:
                    self.primer_archivo = nodo_actual.siguiente
                    if nodo_actual == self.ultimo_archivo:
                        self.ultimo_archivo = None
                return True
            nodo_anterior = nodo_actual
            nodo_actual = nodo_actual.siguiente
        return False

    def mostrar_contenido(self, ruta: str) -> None:
        """
        Método que muestra el contenido de la carpeta en la ruta especificada.

        Parámetros:
        - ruta (str): La ruta de la carpeta a mostrar.

        Retorna:
        - None
        """
        nodo_actual = self.primer_archivo
        if nodo_actual:
            print(f"\n\nDirectorio {ruta}\n\n")
            print("Mode                 LastWriteTime         Length Name")
            print("----                 -------------         ------ ----")

            carpetas = ''
            archivos = ''
            while nodo_actual:
                if isinstance(nodo_actual.dato, Archivo):
                    archivos += f"-a---- {nodo_actual.dato.fecha_hora:>27} {' '*14} {nodo_actual.dato.nombre}\n"
                elif isinstance(nodo_actual.dato, Carpeta):
                    carpetas += f"d----- {nodo_actual.dato.fecha_hora:>27} {' '*14} {nodo_actual.dato.nombre}\n"
                nodo_actual = nodo_actual.siguiente

            print(carpetas[:-1])
            print(archivos[:-1]+"\n\n")

    def to_dict(self) -> dict:
        """
        Convierte la carpeta a un diccionario.

        Retorna:
        - dict: La carpeta convertida a un diccionario.
        """
        archivos = []
        nodo_actual = self.primer_archivo
        while nodo_actual:
            archivos.append(nodo_actual.dato.to_dict())
            nodo_actual = nodo_actual.siguiente
        return {'nombre': self.nombre, 'fecha_hora': self.fecha_hora, 'archivos': archivos}

    @classmethod
    def from_dict(cls, data: dict):
        """
        Crea una instancia de Carpeta a partir de un diccionario.

        Parámetros:
        - data (dict): El diccionario que contiene los datos de la carpeta.

        Retorna:
        - Carpeta: Una nueva instancia de Carpeta creada a partir del diccionario.
        """
        carpeta = cls(data['nombre'], data.get('fecha_hora')
                      )  # Asegurarse de incluir fecha_hora
        for archivo_data in data['archivos']:
            if 'contenido' in archivo_data:  # Es un archivo
                archivo = Archivo.from_dict(archivo_data)
                nodo = Nodo(archivo)
                if not carpeta.primer_archivo:
                    carpeta.primer_archivo = nodo
                    carpeta.ultimo_archivo = nodo
                else:
                    carpeta.ultimo_archivo.siguiente = nodo
                    carpeta.ultimo_archivo = nodo
            else:  # Es una subcarpeta
                subcarpeta = cls.from_dict(archivo_data)
                nodo = Nodo(subcarpeta)
                if not carpeta.primer_archivo:
                    carpeta.primer_archivo = nodo
                    carpeta.ultimo_archivo = nodo
                else:
                    carpeta.ultimo_archivo.siguiente = nodo
                    carpeta.ultimo_archivo = nodo
        return carpeta

    def guardar_json(self, filename: str) -> None:
        """
        Guarda la carpeta y sus archivos en formato JSON.

        Parámetros:
        - filename (str): El nombre del archivo JSON donde se va a guardar la carpeta.

        Retorna:
        - None
        """
        with open(filename, 'w') as f:
            json.dump(self.to_dict(), f, indent=4)

    @classmethod
    def cargar_json(cls, filename: str):
        """
        Carga una carpeta y sus archivos desde un archivo JSON.

        Parámetros:
        - filename (str): El nombre del archivo JSON desde donde se va a cargar la carpeta.

        Retorna:
        - Carpeta: Una nueva instancia de Carpeta cargada desde el archivo JSON.
        """
        with open(filename) as f:
            data = json.load(f)
        return cls.from_dict(data)
