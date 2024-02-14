from pila import Pila
from json import load, dump
from typing import Optional


class Registro:
    def __init__(self) -> None:
        """
        Inicializa una instancia de la clase Registro.
        """
        self.errores: Pila = Pila()
        self.operaciones: Pila = Pila()

    def agregar_error(self, error: str) -> None:
        """
        Agrega un error al registro.

        Parámetros:
        - error (str): El mensaje de error a agregar.

        Retorna:
        - None
        """
        self.errores.push(error)

    def agregar_operacion(self, operacion: str) -> None:
        """
        Agrega una operación al registro.

        Parámetros:
        - operacion (str): La operación realizada a agregar.

        Retorna:
        - None
        """
        self.operaciones.push(operacion)

    def eliminar_ultimo_error(self) -> Optional[str]:
        """
        Elimina y devuelve el último error de la pila de errores.

        Retorna:
        - str | None: El último error eliminado, o None si la pila de errores está vacía.
        """
        return self.errores.pop()
    
    def ver_errores(self) -> list[str]:
        """
        Devuelve una lista con los errores registrados.

        Retorna:
        - List[str]: Lista de mensajes de error.
        """
        return [error for error in self.errores]

    def ver_operaciones(self) -> list[str]:
        """
        Devuelve una lista con las operaciones registradas.

        Retorna:
        - List[str]: Lista de operaciones realizadas.
        """
        return [op for op in self.operaciones]

    def guardar_registros(self, filename: str) -> None:
        """
        Guarda los registros en un archivo JSON.

        Parámetros:
        - filename (str): El nombre del archivo donde se guardarán los registros.

        Retorna:
        - None
        """
        with open(filename, 'w') as f:
            registros = {
                'errores': self.ver_errores(),
                'operaciones': self.ver_operaciones()
            }
            dump(registros, f, indent=4)

    def cargar_registros(self, filename: str) -> None:
        """
        Carga los registros desde un archivo JSON.

        Parámetros:
        - filename (str): El nombre del archivo desde donde se cargarán los registros.

        Retorna:
        - None
        """

        with open(filename, 'r') as f:
            registros = load(f)
            for error in registros['errores']:
                self.errores.push(error)
            for operacion in registros['operaciones']:
                self.operaciones.push(operacion)
