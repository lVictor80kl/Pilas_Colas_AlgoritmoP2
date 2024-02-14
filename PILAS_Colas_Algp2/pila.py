from nodo import Nodo


class Pila:
    def __init__(self) -> None:
        """
        Constructor de la clase Pila.
        """
        self.tope = None

    def push(self, dato) -> None:
        """
        Método que inserta un nuevo elemento en la pila.

        Parámetros:
        - dato: El dato a insertar en la pila.

        Retorna:
        - None
        """
        nuevo_nodo = Nodo(dato)
        nuevo_nodo.siguiente = self.tope
        self.tope = nuevo_nodo

    def pop(self):
        """
        Método que elimina y devuelve el elemento en el tope de la pila.

        Retorna:
        - dato: El dato eliminado del tope de la pila, o None si la pila está vacía.
        """
        if self.tope is None:
            return None
        dato = self.tope.dato
        self.tope = self.tope.siguiente
        return dato

    def __iter__(self):
        nodo_actual = self.tope
        while nodo_actual:
            yield nodo_actual.dato
            nodo_actual = nodo_actual.siguiente
