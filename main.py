# Importación de módulos necesarios para el sistema
from estructuras import ListaEnlazada, ArbolAVLLibros, ArbolSegmentosReportes
from libro import Libro
from usuario import Usuario
from prestamo import Prestamo
import os
import sys
import json
import time

# Definición de la clase principal del sistema de biblioteca
class SistemaBiblioteca:
    def __init__(self):
        """
        Inicializa el sistema de biblioteca con todas las estructuras de datos necesarias.
        """
        # Lista enlazada para almacenar todos los libros
        self.libros = ListaEnlazada()
        # Lista enlazada para almacenar todos los usuarios
        self.usuarios = ListaEnlazada()
        # Lista simple para almacenar todos los préstamos
        self.prestamos = []
        # Contador para generar IDs únicos de préstamos
        self.contador_prestamos = 1
        
        # NUEVOS ÁRBOLES PARA OPTIMIZACIÓN
        # Árbol AVL indexado por ISBN para búsquedas rápidas
        self.arbol_libros_isbn = ArbolAVLLibros('isbn')
        # Árbol AVL indexado por título para búsquedas por título
        self.arbol_libros_titulo = ArbolAVLLibros('titulo')
        # Árbol AVL indexado por autor para búsquedas por autor
        self.arbol_libros_autor = ArbolAVLLibros('autor')
        # Árbol de segmentos para reportes estadísticos por años
        self.arbol_reportes = ArbolSegmentosReportes(list(range(1900, 2024)))
        
        # Agregar datos de ejemplo al sistema
        self.agregar_datos_ejemplo()
        # Construir índices de búsqueda con los datos existentes
        self._construir_indices()
    
    def _construir_indices(self):
        """
        Construye los índices de árboles con los datos existentes.
        Recorre todos los libros y los inserta en los diferentes árboles de índice.
        """
        # Para cada libro en el sistema
        for libro in self.libros.listar():
            # Insertar en árbol indexado por ISBN
            self.arbol_libros_isbn.insertar(libro)
            # Insertar en árbol indexado por título
            self.arbol_libros_titulo.insertar(libro)
            # Insertar en árbol indexado por autor
            self.arbol_libros_autor.insertar(libro)
            # Actualizar estadísticas en el árbol de reportes
            self.arbol_reportes.actualizar_estadisticas(
                libro.año_publicacion, 
                libros=1, 
                prestamos=0
            )
    
    def agregar_datos_ejemplo(self):
        """
        Agrega datos de ejemplo al sistema para pruebas y demostración.
        """
        # Lista de libros de ejemplo
        libros_ejemplo = [
            Libro("978-0142437230", "1984", "George Orwell", 1949, "Ciencia Ficción"),
            Libro("978-0061120084", "To Kill a Mockingbird", "Harper Lee", 1960, "Ficción"),
            Libro("978-0544003415", "The Hobbit", "J.R.R. Tolkien", 1937, "Fantasía"),
            Libro("978-0451524935", "The Great Gatsby", "F. Scott Fitzgerald", 1925, "Ficción"),
            Libro("978-0141439518", "Pride and Prejudice", "Jane Austen", 1813, "Romance")
        ]
        
        # Agregar cada libro de ejemplo al sistema
        for libro in libros_ejemplo:
            self.libros.agregar(libro)
        
        # Lista de usuarios de ejemplo
        usuarios_ejemplo = [
            Usuario("U001", "Juan Pérez", "juan@email.com"),
            Usuario("U002", "María García", "maria@email.com"),
            Usuario("U003", "Carlos Rodríguez", "carlos@email.com"),
            Usuario("U004", "Ana López", "ana@email.com")
        ]
        
        # Agregar cada usuario de ejemplo al sistema
        for usuario in usuarios_ejemplo:
            self.usuarios.agregar(usuario)
    
    # ===== MÉTODOS PARA LIBROS CON ÁRBOLES =====
    
    def agregar_libro(self, isbn, titulo, autor, año_publicacion, genero):
        """
        Agrega un nuevo libro al sistema.
        
        Args:
            isbn (str): ISBN único del libro
            titulo (str): Título del libro
            autor (str): Autor del libro
            año_publicacion (int): Año de publicación
            genero (str): Género del libro
            
        Returns:
            tuple: (éxito, mensaje) indicando si la operación fue exitosa
        """
        # Verificar si ya existe un libro con el mismo ISBN
        if self.buscar_libro_por_isbn(isbn):
            return False, "Ya existe un libro con este ISBN"
        
        # Crear nuevo objeto Libro
        nuevo_libro = Libro(isbn, titulo, autor, año_publicacion, genero)
        # Agregar a la lista principal de libros
        self.libros.agregar(nuevo_libro)
        
        # Actualizar árboles de índice
        self.arbol_libros_isbn.insertar(nuevo_libro)
        self.arbol_libros_titulo.insertar(nuevo_libro)
        self.arbol_libros_autor.insertar(nuevo_libro)
        # Actualizar estadísticas en árbol de reportes
        self.arbol_reportes.actualizar_estadisticas(año_publicacion, libros=1, prestamos=0)
        
        return True, "Libro agregado exitosamente"
    
    def buscar_libro_por_isbn(self, isbn):
        """
        Busca un libro por su ISBN usando el árbol AVL optimizado.
        
        Args:
            isbn (str): ISBN a buscar
            
        Returns:
            Libro: El libro encontrado o None si no existe
        """
        return self.arbol_libros_isbn.buscar(isbn)
    
    def buscar_libros_por_titulo(self, titulo):
        """
        Busca libros por título usando búsqueda por prefijo en árbol AVL.
        
        Args:
            titulo (str): Título o parte del título a buscar
            
        Returns:
            list: Lista de libros que coinciden con el título
        """
        return self.arbol_libros_titulo.buscar_prefijo(titulo.lower())
    
    def buscar_libros_por_autor(self, autor):
        """
        Busca libros por autor usando búsqueda por prefijo en árbol AVL.
        
        Args:
            autor (str): Autor o parte del nombre del autor a buscar
            
        Returns:
            list: Lista de libros que coinciden con el autor
        """
        return self.arbol_libros_autor.buscar_prefijo(autor.lower())
    
    def buscar_libros_por_rango_años(self, año_inicio, año_fin):
        """
        Busca libros publicados en un rango de años específico.
        
        Args:
            año_inicio (int): Año inicial del rango
            año_fin (int): Año final del rango
            
        Returns:
            list: Lista de libros dentro del rango de años
        """
        return [libro for libro in self.libros.listar() 
                if año_inicio <= libro.año_publicacion <= año_fin]
    
    def listar_libros(self):
        """
        Obtiene todos los libros del sistema.
        
        Returns:
            list: Lista de todos los libros
        """
        return self.libros.listar()
    
    def listar_libros_disponibles(self):
        """
        Obtiene todos los libros disponibles para préstamo.
        
        Returns:
            list: Lista de libros disponibles
        """
        return [libro for libro in self.libros.listar() if libro.disponible]
    
    def actualizar_libro(self, isbn, nuevos_datos):
        """
        Actualiza la información de un libro existente.
        
        Args:
            isbn (str): ISBN del libro a actualizar
            nuevos_datos (dict): Diccionario con los campos a actualizar
            
        Returns:
            tuple: (éxito, mensaje) indicando si la operación fue exitosa
        """
        # Buscar el libro por ISBN
        libro = self.buscar_libro_por_isbn(isbn)
        if not libro:
            return False, "Libro no encontrado"
        
        # Actualizar cada campo especificado en nuevos_datos
        for campo, valor in nuevos_datos.items():
            if hasattr(libro, campo):
                setattr(libro, campo, valor)
        
        # Reconstruir índices (simplificado - en producción sería más eficiente)
        self._reconstruir_indices()
        
        return True, "Libro actualizado exitosamente"
    
    def _reconstruir_indices(self):
        """
        Reconstruye todos los índices de árboles desde cero.
        Esto se usa cuando se actualizan muchos libros o hay cambios estructurales.
        """
        # Reinicializar todos los árboles
        self.arbol_libros_isbn = ArbolAVLLibros('isbn')
        self.arbol_libros_titulo = ArbolAVLLibros('titulo')
        self.arbol_libros_autor = ArbolAVLLibros('autor')
        # Volver a construir los índices con los datos actuales
        self._construir_indices()
    
    def eliminar_libro(self, isbn):
        """
        Elimina un libro del sistema.
        
        Args:
            isbn (str): ISBN del libro a eliminar
            
        Returns:
            tuple: (éxito, mensaje) indicando si la operación fue exitosa
        """
        # Verificar si el libro tiene préstamos activos
        prestamos_activos = self.obtener_prestamos_activos_por_libro(isbn)
        if prestamos_activos:
            return False, "No se puede eliminar el libro porque tiene préstamos activos"
        
        # Obtener el libro para actualizar estadísticas
        libro = self.buscar_libro_por_isbn(isbn)
        if libro:
            # Actualizar estadísticas restando un libro
            self.arbol_reportes.actualizar_estadisticas(libro.año_publicacion, libros=-1, prestamos=0)
        
        # Eliminar el libro de la lista principal
        if self.libros.eliminar(lambda libro: libro.isbn == isbn):
            # Reconstruir índices después de la eliminación
            self._reconstruir_indices()
            return True, "Libro eliminado exitosamente"
        else:
            return False, "Libro no encontrado"
    
    # ===== MÉTODOS PARA USUARIOS =====
    
    def agregar_usuario(self, id_usuario, nombre, contacto):
        """
        Agrega un nuevo usuario al sistema.
        
        Args:
            id_usuario (str): ID único del usuario
            nombre (str): Nombre completo del usuario
            contacto (str): Información de contacto (email, teléfono, etc.)
            
        Returns:
            tuple: (éxito, mensaje) indicando si la operación fue exitosa
        """
        # Verificar si ya existe un usuario con el mismo ID
        if self.buscar_usuario_por_id(id_usuario):
            return False, "Ya existe un usuario con este ID"
        
        # Crear nuevo objeto Usuario
        nuevo_usuario = Usuario(id_usuario, nombre, contacto)
        # Agregar a la lista principal de usuarios
        self.usuarios.agregar(nuevo_usuario)
        return True, "Usuario agregado exitosamente"
    
    def buscar_usuario_por_id(self, id_usuario):
        """
        Busca un usuario por su ID.
        
        Args:
            id_usuario (str): ID del usuario a buscar
            
        Returns:
            Usuario: El usuario encontrado o None si no existe
        """
        return self.usuarios.buscar(lambda usuario: usuario.id_usuario == id_usuario)
    
    def buscar_usuarios_por_nombre(self, nombre):
        """
        Busca usuarios por nombre (búsqueda parcial).
        
        Args:
            nombre (str): Nombre o parte del nombre a buscar
            
        Returns:
            list: Lista de usuarios que coinciden con el nombre
        """
        return [usuario for usuario in self.usuarios.listar() if nombre.lower() in usuario.nombre.lower()]
    
    def listar_usuarios(self):
        """
        Obtiene todos los usuarios del sistema.
        
        Returns:
            list: Lista de todos los usuarios
        """
        return self.usuarios.listar()
    
    def actualizar_usuario(self, id_usuario, nuevos_datos):
        """
        Actualiza la información de un usuario existente.
        
        Args:
            id_usuario (str): ID del usuario a actualizar
            nuevos_datos (dict): Diccionario con los campos a actualizar
            
        Returns:
            tuple: (éxito, mensaje) indicando si la operación fue exitosa
        """
        # Buscar el usuario por ID
        usuario = self.buscar_usuario_por_id(id_usuario)
        if not usuario:
            return False, "Usuario no encontrado"
        
        # Actualizar cada campo especificado en nuevos_datos
        for campo, valor in nuevos_datos.items():
            if hasattr(usuario, campo):
                setattr(usuario, campo, valor)
        
        return True, "Usuario actualizado exitosamente"
    
    def eliminar_usuario(self, id_usuario):
        """
        Elimina un usuario del sistema.
        
        Args:
            id_usuario (str): ID del usuario a eliminar
            
        Returns:
            tuple: (éxito, mensaje) indicando si la operación fue exitosa
        """
        # Verificar si el usuario tiene préstamos activos
        prestamos_activos = self.obtener_prestamos_activos_por_usuario(id_usuario)
        if prestamos_activos:
            return False, "No se puede eliminar el usuario porque tiene préstamos activos"
        
        # Eliminar el usuario de la lista principal
        if self.usuarios.eliminar(lambda usuario: usuario.id_usuario == id_usuario):
            return True, "Usuario eliminado exitosamente"
        else:
            return False, "Usuario no encontrado"
    
    # ===== MÉTODOS PARA PRÉSTAMOS =====
    
    def registrar_prestamo(self, isbn_libro, id_usuario, fecha_prestamo):
        """
        Registra un nuevo préstamo en el sistema.
        
        Args:
            isbn_libro (str): ISBN del libro a prestar
            id_usuario (str): ID del usuario que solicita el préstamo
            fecha_prestamo (str): Fecha del préstamo en formato YYYY-MM-DD
            
        Returns:
            tuple: (éxito, mensaje) indicando si la operación fue exitosa
        """
        # Verificar que el libro exista
        libro = self.buscar_libro_por_isbn(isbn_libro)
        if not libro:
            return False, "Libro no encontrado"
        
        # Verificar que el libro esté disponible
        if not libro.disponible:
            return False, "El libro no está disponible"
        
        # Verificar que el usuario exista
        usuario = self.buscar_usuario_por_id(id_usuario)
        if not usuario:
            return False, "Usuario no encontrado"
        
        # Generar ID único para el préstamo
        id_prestamo = f"P{self.contador_prestamos:03d}"
        self.contador_prestamos += 1
        
        # Crear nuevo objeto Préstamo
        nuevo_prestamo = Prestamo(id_prestamo, isbn_libro, id_usuario, fecha_prestamo)
        # Agregar a la lista de préstamos
        self.prestamos.append(nuevo_prestamo)
        
        # Marcar el libro como no disponible
        libro.disponible = False
        
        # Actualizar estadísticas
        año_actual = datetime.now().year
        self.arbol_reportes.actualizar_estadisticas(año_actual, libros=0, prestamos=1)
        
        return True, f"Préstamo registrado exitosamente. ID: {id_prestamo}"
    
    def registrar_devolucion(self, id_prestamo, fecha_devolucion):
        """
        Registra la devolución de un préstamo.
        
        Args:
            id_prestamo (str): ID del préstamo a devolver
            fecha_devolucion (str): Fecha de devolución en formato YYYY-MM-DD
            
        Returns:
            tuple: (éxito, mensaje) indicando si la operación fue exitosa
        """
        # Buscar el préstamo activo por ID
        prestamo = next((p for p in self.prestamos if p.id_prestamo == id_prestamo and p.activo), None)
        if not prestamo:
            return False, "Préstamo no encontrado o ya devuelto"
        
        # Registrar la devolución en el objeto Préstamo
        prestamo.registrar_devolucion(fecha_devolucion)
        
        # Marcar el libro como disponible nuevamente
        libro = self.buscar_libro_por_isbn(prestamo.isbn_libro)
        if libro:
            libro.disponible = True
        
        return True, "Devolución registrada exitosamente"
    
    def obtener_prestamos_activos(self):
        """
        Obtiene todos los préstamos que están activos (no devueltos).
        
        Returns:
            list: Lista de préstamos activos
        """
        return [p for p in self.prestamos if p.activo]
    
    def obtener_prestamos_activos_por_usuario(self, id_usuario):
        """
        Obtiene los préstamos activos de un usuario específico.
        
        Args:
            id_usuario (str): ID del usuario
            
        Returns:
            list: Lista de préstamos activos del usuario
        """
        return [p for p in self.prestamos if p.activo and p.id_usuario == id_usuario]
    
    def obtener_prestamos_activos_por_libro(self, isbn_libro):
        """
        Obtiene los préstamos activos de un libro específico.
        
        Args:
            isbn_libro (str): ISBN del libro
            
        Returns:
            list: Lista de préstamos activos del libro
        """
        return [p for p in self.prestamos if p.activo and p.isbn_libro == isbn_libro]
    
    def listar_todos_los_prestamos(self):
        """
        Obtiene todos los préstamos del sistema (activos e inactivos).
        
        Returns:
            list: Lista completa de préstamos
        """
        return self.prestamos
    
    # ===== MÉTODOS DE REPORTES AVANZADOS =====
    
    def generar_estadisticas_por_año(self, año_inicio, año_fin):
        """
        Genera estadísticas de libros y préstamos para un rango de años.
        
        Args:
            año_inicio (int): Año inicial del rango
            año_fin (int): Año final del rango
            
        Returns:
            dict: Estadísticas agregadas para el rango especificado
        """
        return self.arbol_reportes.consultar_rango(año_inicio, año_fin)
    
    def obtener_libros_mas_antiguos(self, limite=5):
        """
        Obtiene los libros más antiguos del sistema.
        
        Args:
            limite (int): Número máximo de libros a retornar
            
        Returns:
            list: Lista de los libros más antiguos
        """
        # Ordenar libros por año de publicación (ascendente)
        libros_ordenados = sorted(self.libros.listar(), key=lambda x: x.año_publicacion)
        # Retornar los primeros 'limite' libros
        return libros_ordenados[:limite]
    
    def obtener_libros_mas_recientes(self, limite=5):
        """
        Obtiene los libros más recientes del sistema.
        
        Args:
            limite (int): Número máximo de libros a retornar
            
        Returns:
            list: Lista de los libros más recientes
        """
        # Ordenar libros por año de publicación (descendente)
        libros_ordenados = sorted(self.libros.listar(), key=lambda x: x.año_publicacion, reverse=True)
        # Retornar los primeros 'limite' libros
        return libros_ordenados[:limite]
    
    # ===== PERSISTENCIA DE DATOS =====
    
    def guardar_datos(self, archivo='biblioteca_data.json'):
        """
        Guarda todos los datos del sistema en un archivo JSON.
        
        Args:
            archivo (str): Ruta del archivo donde guardar los datos
            
        Returns:
            tuple: (éxito, mensaje) indicando si la operación fue exitosa
        """
        # Preparar diccionario con todos los datos del sistema
        datos = {
            'libros': [libro.to_dict() for libro in self.libros.listar()],
            'usuarios': [usuario.to_dict() for usuario in self.usuarios.listar()],
            'prestamos': [prestamo.to_dict() for prestamo in self.prestamos],
            'contador_prestamos': self.contador_prestamos
        }
        
        try:
            # Escribir datos en archivo JSON
            with open(archivo, 'w', encoding='utf-8') as f:
                json.dump(datos, f, indent=2, ensure_ascii=False)
            return True, "Datos guardados exitosamente"
        except Exception as e:
            return False, f"Error al guardar datos: {str(e)}"
    
    def cargar_datos(self, archivo='biblioteca_data.json'):
        """
        Carga todos los datos del sistema desde un archivo JSON.
        
        Args:
            archivo (str): Ruta del archivo desde donde cargar los datos
            
        Returns:
            tuple: (éxito, mensaje) indicando si la operación fue exitosa
        """
        try:
            # Leer datos desde archivo JSON
            with open(archivo, 'r', encoding='utf-8') as f:
                datos = json.load(f)
            
            # Cargar libros
            self.libros = ListaEnlazada()
            for libro_data in datos['libros']:
                libro = Libro.from_dict(libro_data)
                self.libros.agregar(libro)
            
            # Cargar usuarios
            self.usuarios = ListaEnlazada()
            for usuario_data in datos['usuarios']:
                usuario = Usuario.from_dict(usuario_data)
                self.usuarios.agregar(usuario)
            
            # Cargar préstamos
            self.prestamos = []
            for prestamo_data in datos['prestamos']:
                prestamo = Prestamo.from_dict(prestamo_data)
                self.prestamos.append(prestamo)
            
            # Restaurar contador de préstamos
            self.contador_prestamos = datos['contador_prestamos']
            
            # Reconstruir índices con los datos cargados
            self._reconstruir_indices()
            
            return True, "Datos cargados exitosamente"
        except FileNotFoundError:
            return False, "Archivo de datos no encontrado"
        except Exception as e:
            return False, f"Error al cargar datos: {str(e)}"

# Función para obtener la instancia del sistema
def obtener_sistema():
    """
    Función factory que retorna una instancia del sistema de biblioteca.
    
    Returns:
        SistemaBiblioteca: Instancia del sistema
    """
    return SistemaBiblioteca()

# Clase para pruebas del sistema avanzado
class PruebasSistemaAvanzado:
    def __init__(self):
        """
        Inicializa la clase de pruebas con una instancia del sistema.
        """
        self.sistema = SistemaBiblioteca()

    def prueba_busquedas_optimizadas(self):
        """
        Ejecuta pruebas de rendimiento para las búsquedas optimizadas.
        """
        print("=== Prueba de Búsquedas Optimizadas ===")
        
        # Prueba búsqueda por ISBN
        inicio = time.time()
        libro = self.sistema.buscar_libro_por_isbn("978-0142437230")
        fin = time.time()
        print(f"Búsqueda por ISBN: {libro.titulo if libro else 'No encontrado'}")
        print(f"Tiempo: {fin - inicio:.6f} segundos")
        
        # Prueba búsqueda por título
        inicio = time.time()
        libros = self.sistema.buscar_libros_por_titulo("1984")
        fin = time.time()
        print(f"Búsqueda por título: {len(libros)} resultados")
        print(f"Tiempo: {fin - inicio:.6f} segundos")
        
        # Prueba búsqueda por autor
        inicio = time.time()
        libros = self.sistema.buscar_libros_por_autor("Orwell")
        fin = time.time()
        print(f"Búsqueda por autor: {len(libros)} resultados")
        print(f"Tiempo: {fin - inicio:.6f} segundos")

    def prueba_reportes_avanzados(self):
        """
        Ejecuta pruebas para los reportes estadísticos avanzados.
        """
        print("\n=== Prueba de Reportes Avanzados ===")
        
        # Generar reporte estadístico
        stats = self.sistema.generar_estadisticas_por_año(1900, 2000)
        print(f"Estadísticas 1900-2000: {stats}")
        
        # Libros más antiguos
        antiguos = self.sistema.obtener_libros_mas_antiguos(3)
        print("Libros más antiguos:")
        for libro in antiguos:
            print(f"  - {libro.titulo} ({libro.año_publicacion})")

    def ejecutar_todas_pruebas(self):
        """
        Ejecuta todas las pruebas del sistema.
        """
        self.prueba_busquedas_optimizadas()
        self.prueba_reportes_avanzados()

# Punto de entrada principal
if __name__ == "__main__":
    try:
        # Intentar importar y ejecutar la interfaz gráfica
        from interfaz_grafica import main as gui_main
        gui_main()
    except ImportError as e:
        # Si no se puede cargar la interfaz gráfica, ejecutar pruebas
        print(f"Error: No se pudo cargar la interfaz gráfica: {e}")
        print("Ejecutando pruebas del sistema...")
        pruebas = PruebasSistemaAvanzado()
        pruebas.ejecutar_todas_pruebas()