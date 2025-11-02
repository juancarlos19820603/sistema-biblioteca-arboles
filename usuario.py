class Usuario:
    """
    Clase que representa un usuario en el sistema de gestión de biblioteca.
    Almacena la información básica de los usuarios que pueden realizar préstamos de libros.
    """
    
    def __init__(self, id_usuario, nombre, contacto):
        """
        Inicializa un nuevo usuario en el sistema.
        
        Args:
            id_usuario (str): Identificador único del usuario
            nombre (str): Nombre completo del usuario
            contacto (str): Información de contacto (email, teléfono, etc.)
        """
        # Identificador único del usuario en el sistema
        self.id_usuario = id_usuario
        # Nombre completo del usuario
        self.nombre = nombre
        # Información de contacto (email, teléfono, dirección, etc.)
        self.contacto = contacto
    
    def __str__(self):
        """
        Representación en string del objeto Usuario.
        
        Returns:
            str: Cadena formateada con toda la información del usuario
        """
        # Retornar string formateado con todos los atributos del usuario
        return f"ID: {self.id_usuario}, Nombre: {self.nombre}, Contacto: {self.contacto}"
    
    def to_dict(self):
        """
        Convierte el objeto Usuario a un diccionario para serialización.
        
        Returns:
            dict: Diccionario con todos los atributos del usuario
        """
        # Retornar diccionario con todos los atributos del usuario
        return {
            'id_usuario': self.id_usuario,
            'nombre': self.nombre,
            'contacto': self.contacto
        }
    
    @classmethod
    def from_dict(cls, data):
        """
        Crea un objeto Usuario a partir de un diccionario.
        
        Args:
            data (dict): Diccionario con los datos del usuario
            
        Returns:
            Usuario: Nueva instancia de Usuario creada desde el diccionario
        """
        # Crear y retornar nueva instancia de Usuario con los datos del diccionario
        return cls(
            data['id_usuario'],
            data['nombre'],
            data['contacto']
        )


# Bloque de prueba para verificar el funcionamiento de la clase Usuario
if __name__ == "__main__":
    print("=== Prueba de la clase Usuario ===")
    
    # Crear un usuario de prueba
    usuario_prueba = Usuario("U001", "Juan Pérez", "juan@email.com")
    print(f"Usuario creado: {usuario_prueba}")
    
    # Convertir a diccionario para ver la representación serializada
    dict_usuario = usuario_prueba.to_dict()
    print(f"Representación en diccionario: {dict_usuario}")
    
    # Crear usuario desde diccionario para probar la deserialización
    nuevo_usuario = Usuario.from_dict(dict_usuario)
    print(f"Usuario desde diccionario: {nuevo_usuario}")
    
    print("=== Prueba completada ===")