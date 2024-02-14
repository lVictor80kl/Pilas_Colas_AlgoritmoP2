class Nodo:
    
    def __init__(self, dato):
        """
        Constructor de la clase Nodo.

        Parámetros:
        - dato (Archivo, Carpeta, Pila): El dato que el nodo va a contener. Puede ser un objeto de tipo 'Archivo' o 'Carpeta'.
        """
        self.dato = dato
        self.siguiente = None  # Referencia al siguiente nodo en la lista.
