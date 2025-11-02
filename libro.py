class Libro:
    """
    Clase que representa un libro en el sistema de gestión de biblioteca.
    """
    
    def __init__(self, isbn, titulo, autor, año_publicacion, genero):
        """
        Constructor de la clase Libro.
        
        Args:
            isbn (str): Número único de identificación del libro
            titulo (str): Título del libro
            autor (str): Autor del libro
            año_publicacion (int): Año de publicación del libro
            genero (str): Género literario del libro
        """
        # Asignar el ISBN (Identificador único del libro)
        self.isbn = isbn
        # Asignar el título del libro
        self.titulo = titulo
        # Asignar el autor del libro
        self.autor = autor
        # Asignar el año de publicación del libro
        self.año_publicacion = año_publicacion
        # Asignar el género literario del libro
        self.genero = genero
        # Inicializar el libro como disponible (no prestado)
        self.disponible = True
    
    def __str__(self):
        """
        Representación en string del objeto Libro.
        
        Returns:
            str: Cadena formateada con toda la información del libro
        """
        # Determinar el estado del libro (Disponible o Prestado)
        estado = "Disponible" if self.disponible else "Prestado"
        # Retornar string formateado con todos los atributos del libro
        return f"ISBN: {self.isbn}, Título: {self.titulo}, Autor: {self.autor}, Año: {self.año_publicacion}, Género: {self.genero}, Estado: {estado}"
    
    def cambiar_estado(self):
        """
        Cambia el estado de disponibilidad del libro.
        
        Si estaba disponible lo marca como prestado y viceversa.
        """
        # Invertir el estado de disponibilidad (True -> False, False -> True)
        self.disponible = not self.disponible
    
    def to_dict(self):
        """
        Convierte el objeto Libro a un diccionario.
        
        Returns:
            dict: Diccionario con todos los atributos del libro
        """
        # Retornar diccionario con todos los atributos del libro
        return {
            'isbn': self.isbn,
            'titulo': self.titulo,
            'autor': self.autor,
            'año_publicacion': self.año_publicacion,
            'genero': self.genero,
            'disponible': self.disponible
        }
    
    @classmethod
    def from_dict(cls, data):
        """
        Crea un objeto Libro a partir de un diccionario.
        
        Args:
            data (dict): Diccionario con los datos del libro
            
        Returns:
            Libro: Nueva instancia de Libro creada desde el diccionario
        """
        # Crear una nueva instancia de Libro con los datos básicos del diccionario
        libro = cls(
            data['isbn'],
            data['titulo'],
            data['autor'],
            data['año_publicacion'],
            data['genero']
        )
        # Asignar el estado de disponibilidad desde el diccionario
        libro.disponible = data['disponible']
        # Retornar el libro creado
        return libro


# Bloque de prueba para verificar el funcionamiento de la clase Libro
if __name__ == "__main__":
    print("=== Prueba de la clase Libro ===")
    
    # Crear un libro de prueba
    libro_prueba = Libro("978-0142437230", "1984", "George Orwell", 1949, "Ciencia Ficción")
    print(f"Libro creado: {libro_prueba}")
    
    # Cambiar estado del libro (de disponible a prestado)
    libro_prueba.cambiar_estado()
    print(f"Después de cambiar estado: {libro_prueba}")
    
    # Convertir el libro a diccionario
    dict_libro = libro_prueba.to_dict()
    print(f"Representación en diccionario: {dict_libro}")
    
    # Crear un nuevo libro a partir del diccionario
    nuevo_libro = Libro.from_dict(dict_libro)
    print(f"Libro desde diccionario: {nuevo_libro}")
    
    print("=== Prueba completada ===")