from datetime import datetime, timedelta  # CORREGIDO: agregado timedelta

class Prestamo:
    """
    Clase que representa un préstamo en el sistema de gestión de biblioteca.
    Gestiona el ciclo de vida de un préstamo desde su creación hasta su devolución.
    """
    
    def __init__(self, id_prestamo, isbn_libro, id_usuario, fecha_prestamo):
        """
        Inicializa un nuevo préstamo en el sistema.
        
        Args:
            id_prestamo (str): Identificador único del préstamo
            isbn_libro (str): ISBN del libro prestado
            id_usuario (str): ID del usuario que realiza el préstamo
            fecha_prestamo (str): Fecha del préstamo en formato YYYY-MM-DD
        """
        # Identificador único del préstamo
        self.id_prestamo = id_prestamo
        # ISBN del libro que se está prestando
        self.isbn_libro = isbn_libro
        # ID del usuario que solicita el préstamo
        self.id_usuario = id_usuario
        # Fecha en que se realiza el préstamo
        self.fecha_prestamo = fecha_prestamo
        # Fecha de devolución (inicialmente None hasta que se devuelva)
        self.fecha_devolucion = None
        # Estado del préstamo (True = activo, False = finalizado)
        self.activo = True
    
    def __str__(self):
        """
        Representación en string del objeto Prestamo.
        
        Returns:
            str: Cadena formateada con toda la información del préstamo
        """
        # Determinar el estado del préstamo
        estado = "Activo" if self.activo else "Finalizado"
        # Incluir fecha de devolución si está disponible
        devolucion = f", Devolución: {self.fecha_devolucion}" if self.fecha_devolucion else ""
        # Retornar string formateado con todos los atributos
        return f"ID: {self.id_prestamo}, Libro: {self.isbn_libro}, Usuario: {self.id_usuario}, Préstamo: {self.fecha_prestamo}{devolucion}, Estado: {estado}"
    
    def registrar_devolucion(self, fecha_devolucion=None):
        """
        Registra la devolución del préstamo.
        
        Args:
            fecha_devolucion (str, optional): Fecha de devolución en formato YYYY-MM-DD. 
                                            Si es None, usa la fecha actual.
        """
        # Si no se proporciona fecha, usar la fecha actual
        if fecha_devolucion is None:
            fecha_devolucion = datetime.now().strftime("%Y-%m-%d")
        
        # Establecer fecha de devolución
        self.fecha_devolucion = fecha_devolucion
        # Marcar préstamo como inactivo
        self.activo = False
    
    def to_dict(self):
        """
        Convierte el objeto Prestamo a un diccionario para serialización.
        
        Returns:
            dict: Diccionario con todos los atributos del préstamo
        """
        return {
            'id_prestamo': self.id_prestamo,
            'isbn_libro': self.isbn_libro,
            'id_usuario': self.id_usuario,
            'fecha_prestamo': self.fecha_prestamo,
            'fecha_devolucion': self.fecha_devolucion,
            'activo': self.activo
        }
    
    @classmethod
    def from_dict(cls, data):
        """
        Crea un objeto Prestamo a partir de un diccionario.
        
        Args:
            data (dict): Diccionario con los datos del préstamo
            
        Returns:
            Prestamo: Nueva instancia de Prestamo creada desde el diccionario
        """
        # Crear nueva instancia con los datos básicos
        prestamo = cls(
            data['id_prestamo'],
            data['isbn_libro'],
            data['id_usuario'],
            data['fecha_prestamo']
        )
        # Asignar fecha de devolución desde el diccionario
        prestamo.fecha_devolucion = data['fecha_devolucion']
        # Asignar estado desde el diccionario
        prestamo.activo = data['activo']
        # Retornar el préstamo creado
        return prestamo
    
    def dias_retraso(self):
        """
        Calcula los días de retraso en la devolución del préstamo.
        
        Returns:
            int: Número de días de retraso (0 si no hay retraso o el préstamo está activo)
        """
        # Si el préstamo está activo o no tiene fecha de devolución, no hay retraso
        if self.activo or not self.fecha_devolucion:
            return 0
        
        # Convertir fechas de string a objetos datetime para cálculos
        fecha_prestamo = datetime.strptime(self.fecha_prestamo, "%Y-%m-%d")
        fecha_devolucion = datetime.strptime(self.fecha_devolucion, "%Y-%m-%d")
        
        # Período de préstamo estándar: 15 días
        dias_prestamo = 15
        # Calcular fecha límite para la devolución
        fecha_limite = fecha_prestamo + timedelta(days=dias_prestamo)
        
        # Verificar si hubo retraso
        if fecha_devolucion > fecha_limite:
            # Calcular días de retraso
            retraso = (fecha_devolucion - fecha_limite).days
            return retraso
        
        # No hubo retraso
        return 0


# Bloque de prueba para verificar el funcionamiento de la clase Prestamo
if __name__ == "__main__":
    print("=== Prueba de la clase Prestamo ===")
    
    # Crear un préstamo de prueba
    prestamo_prueba = Prestamo("P001", "978-0142437230", "U001", "2023-10-15")
    print(f"Préstamo creado: {prestamo_prueba}")
    
    # Registrar devolución
    prestamo_prueba.registrar_devolucion("2023-10-25")
    print(f"Después de registrar devolución: {prestamo_prueba}")
    
    # Convertir a diccionario
    dict_prestamo = prestamo_prueba.to_dict()
    print(f"Representación en diccionario: {dict_prestamo}")
    
    # Crear préstamo desde diccionario
    nuevo_prestamo = Prestamo.from_dict(dict_prestamo)
    print(f"Préstamo desde diccionario: {nuevo_prestamo}")
    
    # Probar cálculo de días de retraso
    prestamo_retraso = Prestamo("P002", "978-0061120084", "U002", "2023-10-01")
    prestamo_retraso.registrar_devolucion("2023-10-20")  # 4 días de retraso (15 días de préstamo)
    print(f"Días de retraso: {prestamo_retraso.dias_retraso()}")
    
    print("=== Prueba completada ===")