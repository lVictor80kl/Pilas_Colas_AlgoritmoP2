from archivo import Archivo
from carpeta import Carpeta
from typing import Union
from datetime import datetime
from re import match
from registro import Registro


class Consola():
    def __init__(self, unidad: str, configuracion: dict):
        # Obtener la fecha y hora actual
        fecha_actual = datetime.now()

        # Formatear la fecha y hora en el formato deseado
        fecha_formateada = fecha_actual.strftime("%d/%m/%Y %I:%M %p")

        self.unidad: Carpeta = Carpeta(unidad, fecha_formateada)

        self.filename_unidad = configuracion['ruta_unidades'] + \
            '/' + configuracion['unidades'][0]['nombre_archivo']

        self.filename_operaciones_errores = configuracion['ruta_operaciones_errores'] + \
            '/' + configuracion['nombre_archivo_operaciones_errores']

        self.filename_respaldo = configuracion['ruta_respaldo']+'/'

        self.registro = Registro()

        # Ruta actual (La que se mostrará en consola)
        self.ruta_actual: str = unidad
        self.cargar()
        self.ejecutar()

    def cargar(self) -> None:
        """
        Carga la estructura de carpetas, errores, operaciones y respaldo desde un archivo JSON o crea uno nuevo si no existe.

        Retorna:
        - None
        """
        try:
            # Intentar cargar la estructura de la carpeta principal desde el archivo JSON
            self.unidad: Carpeta = Carpeta.cargar_json(self.filename_unidad)
        except FileNotFoundError:
            # Si no se encuentra el archivo, imprimir un mensaje y crear una nueva unidad
            print(
                f"No se encontró el archivo '{self.filename_unidad}'. Se creará un nuevo archivo para la unidad {self.unidad.nombre}.")
            self.unidad.guardar_json(self.filename_unidad)

        try:
            # Intentar cargar la estructura de la carpeta principal desde el archivo JSON
            self.registro.cargar_registros(self.filename_operaciones_errores)
        except FileNotFoundError:
            # Si no se encuentra el archivo, imprimir un mensaje y crear una nueva unidad
            print(
                f"No se encontró el archivo '{self.filename_operaciones_errores}'. Se creará un nuevo archivo para las operaciones y errores.")
            self.registro.guardar_registros(self.filename_operaciones_errores)

    def ejecutar(self):
        while True:
            entrada = input(f"{self.ruta_actual}\>" if self.ruta_actual ==
                            self.unidad.nombre else f"{self.ruta_actual}>").strip()
            try:
                self.comando(entrada)
                # Obtener la fecha y hora actual
                fecha_actual = datetime.now()

                # Formatear la fecha y hora en el formato deseado
                fecha_formateada = fecha_actual.strftime("%d/%m/%Y %I:%M %p")

                self.registro.agregar_operacion(
                    f"fecha: {fecha_formateada} - entrada: {entrada}")

                self.registro.guardar_registros(
                    self.filename_operaciones_errores)

            except Exception as e:
                print(f"{e}")
                # Obtener la fecha y hora actual
                fecha_actual = datetime.now()

                # Formatear la fecha y hora en el formato deseado
                fecha_formateada = fecha_actual.strftime("%d/%m/%Y %I:%M %p")

                self.registro.agregar_error(
                    f'fecha: {fecha_formateada} - entrada: {entrada} - error: {e}')

                self.registro.guardar_registros(
                    self.filename_operaciones_errores)

    def comando(self, entrada: str):
        """
        Método que ejecuta comandos ingresados por el usuario en la consola.

        Parámetros:
        - entrada (str): La entrada ingresada por el usuario en la consola.

        No retorna ningún valor.
        """
        if entrada.lower() == "exit":
            print("Saliendo de la consola...")
            exit()

        elif entrada.lower() == "clear log":
            error_eliminado = self.registro.eliminar_ultimo_error()
            if error_eliminado:
                print("Se ha eliminado el último error.")
                print(f"{error_eliminado}")
            else:
                print("Historial de errores vacío.")
            return

        elif entrada.lower() == "log":
            print("Historial de errores: ")
            for error in self.registro.ver_errores():
                print(error)

            print("")

            print("Historial de operaciones")
            for operacion in self.registro.ver_operaciones():
                print(operacion)
            return

        partes_entrada = entrada.split(" ")
        comando = partes_entrada[0].lower()
        argumentos = partes_entrada[1:]

        if comando == "cd":
            if len(argumentos) != 1:
                raise ValueError("Uso incorrecto del comando. Uso: cd ruta")
            self.cd(argumentos[0])

        elif comando == "mkdir":
            if len(argumentos) != 1:
                raise ValueError("Uso incorrecto del comando. Uso: mkdir ruta")
            self.mkdir(argumentos[0])

        elif comando == "type":
            if len(entrada.split(" ", 2)) != 3:
                raise ValueError(
                    "Uso incorrecto del comando. Uso: type ruta contenido")

            argumentos = entrada.split(" ", 1)[1]
            if not ' "' in argumentos or argumentos.count('"') != 2:
                raise ValueError(
                    'Uso incorrecto del comando. Uso: type ruta "contenido"')

            # Dividir en dos partes, máximo 1 división
            ruta, contenido = argumentos.split(' "', 1)
            # Eliminar la comilla al final del contenido
            contenido = contenido.rstrip('"')
            self.type(ruta, contenido)

        elif comando == "rmdir":
            if len(argumentos) != 1:
                raise ValueError("Uso incorrecto del comando. Uso: rmdir ruta")
            self.rmdir(argumentos[0])

        elif comando == "dir":
            if len(argumentos) > 1:
                raise ValueError("Uso incorrecto del comando. Uso: dir [ruta]")
            self.dir(argumentos if not argumentos else argumentos[0])

        else:
            raise ValueError(
                "Comando no reconocido. Los comandos disponibles son: cd, mkdir, type, rmdir, dir, exit, log")

    def type(self, ruta: str, contenido: str):
        """
        Método que crea un nuevo archivo con el contenido especificado en la ruta especificada.

        Parámetros:
        - ruta (str): La ruta donde se creará el nuevo archivo.
        - contenido (str): El contenido del archivo a crear.

        No retorna ningún valor.
        """
        campos = ruta.split("/")
        nombre_archivo = campos[-1].strip()

        ruta_archivo = '/'.join(campos[:-1])

        if not ruta_archivo:  # Se crea la carpeta en el directorio actual
            nodo = self.obtener_nodo_ruta_actual()

        elif ':' in ruta_archivo:
            aux = self.ruta_actual
            self.ruta_actual = self.unidad.nombre
            nodo = self.obtener_nodo_ruta_actual()
            self.ruta_actual = aux

            ruta_partes = ruta_archivo.split("/")[1:]

            for parte in ruta_partes:
                nodo = nodo.buscar_carpeta(parte)
                if not nodo:
                    raise ValueError("La ruta especificada no existe.")

        else:
            nodo = self.obtener_nodo_ruta_actual()

            ruta_partes = ruta_archivo.split("/")

            for parte in ruta_partes:
                nodo = nodo.buscar_carpeta(parte)
                if not nodo:
                    raise ValueError("La ruta especificada no existe.")

        if nombre_archivo[-4:] != ".txt":
            raise ValueError(
                "El nombre del archivo no posee la extensión '.txt'.")

        nombre_sin_extension = nombre_archivo[:-4]

        if not nombre_sin_extension:
            raise ValueError("El nombre no puede quedar vacío.")

        if not self.contiene_caracteres_validos(nombre_sin_extension):
            raise ValueError(
                "Nombre con caracteres inválidos. Caracteres permitidos: letras de la a-z y A-Z,espacios en blanco y números del 0 al 9.")

        if nodo.buscar_archivo(nombre_archivo):
            raise ValueError("Ya existe un archivo con ese mismo nombre.")

        # Obtener la fecha y hora actual
        fecha_actual = datetime.now()
        # Formatear la fecha y hora en el formato deseado
        fecha_formateada = fecha_actual.strftime("%d/%m/%Y %I:%M %p")

        nodo.crear_archivo(nombre_archivo, contenido, fecha_formateada)
        ruta_archivo = self.ruta_actual if not ruta_archivo else self.ruta_actual+'\\' + \
            ruta_archivo.replace(
                '/', '\\') if not ':' in ruta_archivo else ruta_archivo.replace('/', '\\')
        print(
            f"Archivo '{nombre_archivo}' creado correctamente en {ruta_archivo}")
        self.unidad.guardar_json(self.filename_unidad)

    def mkdir(self, ruta: str):
        """
        Método que crea una nueva carpeta en la ruta especificada.

        Parámetros:
        - ruta (str): La ruta donde se creará la nueva carpeta.

        No retorna ningún valor.
        """
        campos = ruta.split("/")
        nombre_carpeta = campos[-1].strip()
        ruta_carpeta = '/'.join(campos[:-1])

        if not ruta_carpeta:  # Se crea la carpeta en el directorio actual
            nodo = self.obtener_nodo_ruta_actual()

        elif ':' in ruta_carpeta:
            aux = self.ruta_actual
            self.ruta_actual = self.unidad.nombre
            nodo = self.obtener_nodo_ruta_actual()
            self.ruta_actual = aux

            ruta_partes = ruta_carpeta.split("/")[1:]

            for parte in ruta_partes:
                nodo = nodo.buscar_carpeta(parte)
                if not nodo:
                    raise ValueError("La ruta especificada no existe.")

        else:
            nodo = self.obtener_nodo_ruta_actual()

            ruta_partes = ruta_carpeta.split("/")

            for parte in ruta_partes:
                nodo = nodo.buscar_carpeta(parte)
                if not nodo:
                    raise ValueError("La ruta especificada no existe.")

        if not nombre_carpeta:
            raise ValueError("El nombre no puede quedar vacío.")

        if not self.contiene_caracteres_validos(nombre_carpeta):
            raise ValueError(
                "Nombre con caracteres inválidos. Caracteres permitidos: letras de la a-z y A-Z,espacios en blanco y números del 0 al 9.")

        if nodo.buscar_carpeta(nombre_carpeta):
            raise ValueError("Ya existe una carpeta con ese mismo nombre.")

        # Obtener la fecha y hora actual
        fecha_actual = datetime.now()
        # Formatear la fecha y hora en el formato deseado
        fecha_formateada = fecha_actual.strftime("%d/%m/%Y %I:%M %p")

        nodo.crear_carpeta(nombre_carpeta, fecha_formateada)

        ruta_carpeta = self.ruta_actual if not ruta_carpeta else self.ruta_actual+'\\' + \
            ruta_carpeta.replace(
                '/', '\\') if not ':' in ruta_carpeta else ruta_carpeta.replace('/', '\\')
        print(
            f"Carpeta '{nombre_carpeta}' creada correctamente en {ruta_carpeta}")
        self.unidad.guardar_json(self.filename_unidad)

    def rmdir(self, ruta: str):
        """
        Método que elimina una carpeta especificada por la ruta.

        Parámetros:
        - ruta (str): La ruta de la carpeta a eliminar.

        No retorna ningún valor.
        """
        campos = ruta.split("/")
        nombre_carpeta = campos[-1].strip()
        ruta_carpeta = '/'.join(campos[:-1])

        if not ruta_carpeta:  # Directorio actual
            nodo = self.obtener_nodo_ruta_actual()

        elif ':' in ruta_carpeta:
            aux = self.ruta_actual
            self.ruta_actual = self.unidad.nombre
            nodo = self.obtener_nodo_ruta_actual()
            self.ruta_actual = aux

            ruta_partes = ruta_carpeta.split("/")[1:]

            for parte in ruta_partes:
                nodo = nodo.buscar_carpeta(parte)
                if not nodo:
                    raise ValueError("La ruta especificada no existe.")

        else:
            nodo = self.obtener_nodo_ruta_actual()

            ruta_partes = ruta_carpeta.split("/")

            for parte in ruta_partes:
                nodo = nodo.buscar_carpeta(parte)
                if not nodo:
                    raise ValueError("La ruta especificada no existe.")

        if not nombre_carpeta:
            raise ValueError("El nombre no puede quedar vacío.")

        if not self.contiene_caracteres_validos(nombre_carpeta):
            raise ValueError(
                "Nombre con caracteres inválidos. Caracteres permitidos: letras de la a-z y A-Z,espacios en blanco y números del 0 al 9.")

        ruta_carpeta = self.ruta_actual if not ruta_carpeta else self.ruta_actual+'\\' + \
            ruta_carpeta.replace(
                '/', '\\') if not ':' in ruta_carpeta else ruta_carpeta.replace('/', '\\')

        if not nodo.buscar_carpeta(nombre_carpeta):
            raise ValueError(
                f"No se pudo encontrar la carpeta '{nombre_carpeta}' en {ruta_carpeta}")

        nombre_respaldo: str = ''
        nombre_respaldo += self.filename_respaldo
        nombre_respaldo += f"Eliminación de carpeta '{nombre_carpeta}' en Unidad {self.unidad.nombre[:-1]}"
        nombre_respaldo += ".json"

        # Respaldamos antes de borrar la carpeta
        self.unidad.guardar_json(nombre_respaldo)

        nodo.eliminar_carpeta(nombre_carpeta)

        print(
            f"Carpeta '{nombre_carpeta}' eliminada correctamente de {ruta_carpeta}")
        self.unidad.guardar_json(self.filename_unidad)

    def contiene_caracteres_validos(self, cadena: str):
        """
        Verifica si una cadena contiene solo caracteres válidos: letras de la a-z y A-Z,
        espacios en blanco y números del 0 al 9.

        Parámetros:
        - cadena (str): La cadena a verificar.

        Retorna:
        - bool: True si la cadena contiene solo caracteres válidos, False en caso contrario.
        """
        # Patrón para caracteres válidos: letras de la a-z y A-Z, espacios en blanco y números del 0 al 9
        patron = r'^[a-zA-Z0-9\s]*$'

        # Verificar si la cadena coincide con el patrón
        if match(patron, cadena):
            return True
        else:
            return False

    def dir(self, ruta: str):
        """
        Método que muestra el contenido de la carpeta en la ruta especificada.

        Parámetros:
        - ruta (str): La ruta de la carpeta a mostrar.

        No retorna ningún valor.
        """

        if not ruta:
            nodo = self.obtener_nodo_ruta_actual()
            nodo.mostrar_contenido(self.ruta_actual)

        elif ":" in ruta:
            aux = self.ruta_actual
            self.ruta_actual = self.unidad.nombre
            nodo = self.obtener_nodo_ruta_actual()
            self.ruta_actual = aux

            ruta_partes = ruta.split("/")[1:]

            for parte in ruta_partes:
                nodo = nodo.buscar_carpeta(parte)
                if not nodo:
                    raise ValueError("La ruta especificada no existe.")
            nodo.mostrar_contenido(ruta.replace('/', '\\'))

        else:
            nodo = self.obtener_nodo_ruta_actual()

            ruta_partes = ruta.split("/")

            for parte in ruta_partes:
                nodo = nodo.buscar_carpeta(parte)
                if not nodo:
                    raise ValueError("La ruta especificada no existe.")
            nodo.mostrar_contenido(
                self.ruta_actual+"\\" + ruta.replace("/", "\\"))

    def cd(self, ruta: str):
        """
        Cambia el directorio actual a la ruta especificada.

        Parámetros:
        - ruta (str): La ruta a la que se desea cambiar el directorio actual.

        No retorna ningún valor.
        """
        # Caso: cd  ..  (Regresa  al  directorio  padre)
        if ruta == "..":
            nodo = self.obtener_nodo_padre()
            if nodo and nodo.nombre == self.unidad.nombre:
                self.ruta_actual = self.unidad.nombre

            elif nodo:
                componentes_ruta = self.ruta_actual.split('\\')
                self.ruta_actual = '\\'.join(componentes_ruta[:-1])

        # Caso: cd C:/Documentos/Proyectos
        elif ":" in ruta:
            aux = self.ruta_actual
            self.ruta_actual = self.unidad.nombre
            nodo = self.obtener_nodo_ruta_actual()
            self.ruta_actual = aux

            ruta_partes = ruta.split("/")[1:]

            for parte in ruta_partes:
                nodo = nodo.buscar_carpeta(parte)
                if not nodo:
                    raise ValueError("La ruta especificada no existe.")

            self.ruta_actual = ruta.replace("/", "\\")

        # Casso: cd  /usuario/nombre_de_usuario  (Cambia  a  una  ruta  absoluta)
        else:
            nodo = self.obtener_nodo_ruta_actual()

            ruta_partes = ruta.split("/")

            for parte in ruta_partes:
                nodo = nodo.buscar_carpeta(parte)
                if not nodo:
                    raise ValueError("La ruta especificada no existe.")

            self.ruta_actual += "\\" + ruta.replace("/", "\\")

    def obtener_nodo_padre(self) -> Union[None, Carpeta]:
        """
        Obtiene el nodo padre de la carpeta actual.

        Retorna:
        - Carpeta | None: La carpeta padre si existe, None si la carpeta actual es la raíz.
        """
        # Dividir la ruta actual en componentes separados por '\'
        componentes_ruta = self.ruta_actual.split(
            '\\')  # Tipo de datos esperado: str

        # Eliminar el último componente de la ruta (nombre de la carpeta actual)
        # Tipo de datos esperado: str
        ruta_padre = '\\'.join(componentes_ruta[:-1])
        # Si la ruta padre está vacía, significa que la ruta actual es la raíz y no tiene un nodo padre
        if not ruta_padre:
            return None
        # Realizar una búsqueda en la estructura de carpetas a partir de la ruta padre
        # Tipo de datos esperado: Carpeta (suposición)
        nodo_actual = self.unidad
        # Tipo de datos esperado: str
        for componente in ruta_padre.split('\\'):
            if componente != self.unidad.nombre:
                # Tipo de datos esperado: Union[None, Carpeta]
                nodo_actual = nodo_actual.buscar_carpeta(componente)
        return nodo_actual  # Tipo de datos esperado: Union[None, Carpeta]

    def obtener_nodo_ruta_actual(self) -> Carpeta:
        """
        Obtiene el nodo correspondiente a la ruta actual.

        Retorna:
        - Carpeta: La carpeta correspondiente a la ruta actual.
        """
        componentes_ruta = self.ruta_actual.split(
            '\\')  # Tipo de datos esperado: str

        ruta = '\\'.join(componentes_ruta[1:])  # Tipo de datos esperado: str

        if not ruta:
            return self.unidad  # Si la ruta está vacía, devuelve None

        # Tipo de datos esperado: Carpeta (suposición)
        nodo_actual = self.unidad
        for componente in ruta.split('\\'):  # Tipo de datos esperado: str
            # Tipo de datos esperado: Union[None, Carpeta]
            nodo_actual = nodo_actual.buscar_carpeta(componente)
        return nodo_actual  # Tipo de datos esperado: Carpeta
