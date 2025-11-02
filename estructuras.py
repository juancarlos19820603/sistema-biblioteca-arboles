class Nodo:
    """
    Clase que representa un nodo en una lista enlazada.
    """
    
    def __init__(self, dato):
        # Constructor del nodo - inicializa con un dato y sin nodo siguiente
        self.dato = dato  # Almacena el dato en el nodo
        self.siguiente = None  # Inicialmente no hay siguiente nodo (None)


class ListaEnlazada:
    """
    Clase que representa una lista enlazada simple.
    """
    
    def __init__(self):
        # Constructor de la lista - inicializa una lista vacía
        self.cabeza = None  # La lista comienza sin cabeza (vacía)
        self.tamanio = 0    # Contador para llevar el tamaño de la lista
    
    def esta_vacia(self):
        # Verifica si la lista está vacía
        return self.cabeza is None  # Retorna True si cabeza es None (lista vacía)
    
    def agregar(self, dato):
        # Agrega un nuevo elemento al FINAL de la lista
        nuevo_nodo = Nodo(dato)  # Crea un nuevo nodo con el dato
        
        if self.esta_vacia():
            # Si la lista está vacía, el nuevo nodo se convierte en la cabeza
            self.cabeza = nuevo_nodo
        else:
            # Si no está vacía, recorre hasta el último nodo
            actual = self.cabeza  # Comienza desde la cabeza
            while actual.siguiente is not None:
                # Avanza hasta encontrar el último nodo (que tiene siguiente = None)
                actual = actual.siguiente
            # Enlaza el último nodo con el nuevo nodo
            actual.siguiente = nuevo_nodo
        
        self.tamanio += 1  # Incrementa el contador de tamaño
    
    def eliminar(self, criterio):
        # Elimina el PRIMER elemento que cumpla con el criterio
        if self.esta_vacia():
            # Si la lista está vacía, no hay nada que eliminar
            return False
        
        if criterio(self.cabeza.dato):
            # Si el primer nodo (cabeza) cumple el criterio
            self.cabeza = self.cabeza.siguiente  # La nueva cabeza es el siguiente nodo
            self.tamanio -= 1  # Decrementa el tamaño
            return True  # Retorna éxito
        
        # Busca en el resto de la lista
        actual = self.cabeza
        while actual.siguiente is not None:
            # Verifica si el siguiente nodo cumple el criterio
            if criterio(actual.siguiente.dato):
                # Salta el nodo a eliminar, enlazando con el siguiente del siguiente
                actual.siguiente = actual.siguiente.siguiente
                self.tamanio -= 1  # Decrementa el tamaño
                return True  # Retorna éxito
            actual = actual.siguiente  # Avanza al siguiente nodo
        
        return False  # No se encontró ningún elemento que cumpla el criterio
    
    def buscar(self, criterio):
        # Busca el PRIMER elemento que cumpla con el criterio
        actual = self.cabeza  # Comienza desde la cabeza
        while actual is not None:
            # Recorre todos los nodos
            if criterio(actual.dato):
                # Si encuentra un nodo que cumple el criterio, retorna su dato
                return actual.dato
            actual = actual.siguiente  # Avanza al siguiente nodo
        
        return None  # No se encontró ningún elemento
    
    def listar(self):
        # Retorna todos los elementos de la lista como una lista Python
        elementos = []  # Lista vacía para almacenar los elementos
        actual = self.cabeza  # Comienza desde la cabeza
        
        while actual is not None:
            # Recorre todos los nodos y agrega sus datos a la lista
            elementos.append(actual.dato)
            actual = actual.siguiente  # Avanza al siguiente nodo
        
        return elementos  # Retorna la lista completa
    
    def actualizar(self, criterio, nuevos_datos):
        # Actualiza el PRIMER elemento que cumpla con el criterio
        elemento = self.buscar(criterio)  # Busca el elemento
        if elemento:
            # Si encontró el elemento, actualiza sus campos
            for clave, valor in nuevos_datos.items():
                # Para cada campo en nuevos_datos
                if hasattr(elemento, clave):
                    # Verifica que el elemento tenga ese atributo
                    setattr(elemento, clave, valor)  # Asigna el nuevo valor
            return True  # Retorna éxito
        
        return False  # No se encontró el elemento
    
    def __str__(self):
        # Representación en string de la lista (para debugging)
        elementos = []  # Lista para almacenar los strings de cada dato
        actual = self.cabeza  # Comienza desde la cabeza
        
        while actual is not None:
            # Convierte cada dato a string y lo agrega a la lista
            elementos.append(str(actual.dato))
            actual = actual.siguiente  # Avanza al siguiente nodo
        
        # Une todos los strings con " -> " o muestra "Lista vacía"
        return " -> ".join(elementos) if elementos else "Lista vacía"


# ================= ESTRUCTURAS DE ÁRBOLES =================

class NodoAVL:
    # Nodo para árbol AVL - almacena libro y clave para búsqueda
    def __init__(self, clave, libro):
        self.clave = clave      # Clave para ordenar (ISBN, título o autor)
        self.libro = libro      # Objeto Libro almacenado
        self.izquierda = None   # Hijo izquierdo
        self.derecha = None     # Hijo derecho
        self.altura = 1         # Altura del nodo (para balanceo AVL)

class ArbolAVLLibros:
    # Árbol AVL balanceado para búsquedas eficientes de libros
    def __init__(self, tipo_clave='isbn'):
        self.raiz = None           # Raíz del árbol
        self.tipo_clave = tipo_clave  # Tipo de clave: 'isbn', 'titulo' o 'autor'
    
    def obtener_clave(self, libro):
        # Obtiene la clave apropiada según el tipo configurado
        if self.tipo_clave == 'isbn':
            return libro.isbn              # Retorna ISBN como clave
        elif self.tipo_clave == 'titulo':
            return libro.titulo.lower()    # Retorna título en minúsculas
        elif self.tipo_clave == 'autor':
            return libro.autor.lower()     # Retorna autor en minúsculas
        return libro.isbn  # Por defecto usa ISBN
    
    def _obtener_altura(self, nodo):
        # Obtiene la altura de un nodo (0 si el nodo es None)
        if not nodo:
            return 0
        return nodo.altura  # Retorna la altura almacenada en el nodo
    
    def _obtener_balance(self, nodo):
        # Calcula el factor de balance (altura izquierda - altura derecha)
        if not nodo:
            return 0  # Nodo vacío tiene balance 0
        return self._obtener_altura(nodo.izquierda) - self._obtener_altura(nodo.derecha)
    
    def _rotar_derecha(self, z):
        # Rotación simple a la derecha para balancear el árbol
        y = z.izquierda    # y es el hijo izquierdo de z
        T3 = y.derecha     # T3 es el subárbol derecho de y
        
        # Realiza la rotación
        y.derecha = z      # z se convierte en hijo derecho de y
        z.izquierda = T3   # T3 se convierte en hijo izquierdo de z
        
        # Actualiza alturas después de la rotación
        z.altura = 1 + max(self._obtener_altura(z.izquierda), 
                          self._obtener_altura(z.derecha))
        y.altura = 1 + max(self._obtener_altura(y.izquierda), 
                          self._obtener_altura(y.derecha))
        
        return y  # Retorna la nueva raíz del subárbol
    
    def _rotar_izquierda(self, z):
        # Rotación simple a la izquierda para balancear el árbol
        y = z.derecha      # y es el hijo derecho de z
        T2 = y.izquierda   # T2 es el subárbol izquierdo de y
        
        # Realiza la rotación
        y.izquierda = z    # z se convierte en hijo izquierdo de y
        z.derecha = T2     # T2 se convierte en hijo derecho de z
        
        # Actualiza alturas después de la rotación
        z.altura = 1 + max(self._obtener_altura(z.izquierda), 
                          self._obtener_altura(z.derecha))
        y.altura = 1 + max(self._obtener_altura(y.izquierda), 
                          self._obtener_altura(y.derecha))
        
        return y  # Retorna la nueva raíz del subárbol
    
    def insertar(self, libro):
        # Inserta un libro en el árbol (método público)
        clave = self.obtener_clave(libro)  # Obtiene la clave del libro
        self.raiz = self._insertar(self.raiz, clave, libro)  # Inserta recursivamente
    
    def _insertar(self, nodo, clave, libro):
        # Inserta recursivamente en el árbol AVL
        if not nodo:
            # Si llegamos a un nodo vacío, creamos uno nuevo
            return NodoAVL(clave, libro)
        
        # Inserta en el subárbol apropiado
        if clave < nodo.clave:
            # Si la clave es menor, inserta en el subárbol izquierdo
            nodo.izquierda = self._insertar(nodo.izquierda, clave, libro)
        else:
            # Si la clave es mayor o igual, inserta en el subárbol derecho
            nodo.derecha = self._insertar(nodo.derecha, clave, libro)
        
        # Actualiza la altura del nodo actual
        nodo.altura = 1 + max(self._obtener_altura(nodo.izquierda), 
                             self._obtener_altura(nodo.derecha))
        
        # Calcula el factor de balance
        balance = self._obtener_balance(nodo)
        
        # Caso 1: Rotación simple derecha (izquierda-izquierda)
        if balance > 1 and clave < nodo.izquierda.clave:
            return self._rotar_derecha(nodo)
        
        # Caso 2: Rotación simple izquierda (derecha-derecha)
        if balance < -1 and clave > nodo.derecha.clave:
            return self._rotar_izquierda(nodo)
        
        # Caso 3: Rotación doble izquierda-derecha
        if balance > 1 and clave > nodo.izquierda.clave:
            nodo.izquierda = self._rotar_izquierda(nodo.izquierda)
            return self._rotar_derecha(nodo)
        
        # Caso 4: Rotación doble derecha-izquierda
        if balance < -1 and clave < nodo.derecha.clave:
            nodo.derecha = self._rotar_derecha(nodo.derecha)
            return self._rotar_izquierda(nodo)
        
        return nodo  # Retorna el nodo (posiblemente balanceado)
    
    def buscar(self, clave):
        # Búsqueda pública de un libro por clave exacta
        return self._buscar(self.raiz, clave.lower() if isinstance(clave, str) else clave)
    
    def _buscar(self, nodo, clave):
        # Búsqueda recursiva en el árbol
        if not nodo:
            return None  # No se encontró
        
        if clave == nodo.clave:
            return nodo.libro  # Encontró el libro
        elif clave < nodo.clave:
            # Busca en el subárbol izquierdo
            return self._buscar(nodo.izquierda, clave)
        else:
            # Busca en el subárbol derecho
            return self._buscar(nodo.derecha, clave)
    
    def buscar_prefijo(self, prefijo):
        # Búsqueda de todos los libros que empiecen con un prefijo
        resultados = []  # Lista para almacenar resultados
        self._buscar_prefijo(self.raiz, prefijo.lower(), resultados)  # Búsqueda recursiva
        return resultados
    
    def _buscar_prefijo(self, nodo, prefijo, resultados):
        # Búsqueda recursiva por prefijo
        if not nodo:
            return  # Nodo vacío, termina recursión
        
        if nodo.clave.startswith(prefijo):
            # Si la clave empieza con el prefijo, agrega a resultados
            resultados.append(nodo.libro)
        
        # Decide en qué subárboles continuar la búsqueda
        if prefijo <= nodo.clave:
            # Si el prefijo es menor o igual, busca en izquierdo
            self._buscar_prefijo(nodo.izquierda, prefijo, resultados)
        
        if prefijo >= nodo.clave[:len(prefijo)]:
            # Si el prefijo es mayor o igual al inicio de la clave, busca en derecho
            self._buscar_prefijo(nodo.derecha, prefijo, resultados)

class NodoSegmento:
    # Nodo para árbol de segmentos (para reportes estadísticos)
    def __init__(self, inicio, fin):
        self.inicio = inicio          # Inicio del rango (año)
        self.fin = fin                # Fin del rango (año)
        self.total_libros = 0         # Total de libros en este rango
        self.total_prestamos = 0      # Total de préstamos en este rango
        self.izquierda = None         # Hijo izquierdo (subrango menor)
        self.derecha = None           # Hijo derecho (subrango mayor)

class ArbolSegmentosReportes:
    # Árbol de segmentos para consultas eficientes de rango
    def __init__(self, años):
        self.años = años              # Lista de años a cubrir
        self.raiz = self._construir_arbol(0, len(años)-1)  # Construye el árbol
    
    def _construir_arbol(self, inicio, fin):
        # Construye recursivamente el árbol de segmentos
        if inicio > fin:
            return None  # Caso base: rango inválido
        
        # Crea un nodo que representa el rango [años[inicio], años[fin]]
        nodo = NodoSegmento(self.años[inicio], self.años[fin])
        
        if inicio == fin:
            return nodo  # Caso base: nodo hoja (rango de un solo año)
        
        # Divide el rango en dos mitades
        medio = (inicio + fin) // 2
        # Construye subárbol izquierdo y derecho recursivamente
        nodo.izquierda = self._construir_arbol(inicio, medio)
        nodo.derecha = self._construir_arbol(medio + 1, fin)
        
        return nodo  # Retorna el nodo construido
    
    def actualizar_estadisticas(self, año, libros=0, prestamos=0):
        # Actualiza las estadísticas para un año específico
        self._actualizar(self.raiz, año, libros, prestamos)
    
    def _actualizar(self, nodo, año, libros, prestamos):
        # Actualiza recursivamente las estadísticas
        if not nodo or año < nodo.inicio or año > nodo.fin:
            return  # Año fuera del rango del nodo
        
        # Actualiza los contadores del nodo
        nodo.total_libros += libros
        nodo.total_prestamos += prestamos
        
        # Propaga la actualización a los hijos
        if nodo.izquierda:
            self._actualizar(nodo.izquierda, año, libros, prestamos)
        if nodo.derecha:
            self._actualizar(nodo.derecha, año, libros, prestamos)
    
    def consultar_rango(self, inicio, fin):
        # Consulta pública para un rango de años
        return self._consultar_rango(self.raiz, inicio, fin)
    
    def _consultar_rango(self, nodo, inicio, fin):
        # Consulta recursiva de estadísticas por rango
        if not nodo or inicio > nodo.fin or fin < nodo.inicio:
            # Rango no se superpone con el nodo
            return {'total_libros': 0, 'total_prestamos': 0}
        
        if inicio <= nodo.inicio and fin >= nodo.fin:
            # El rango del nodo está completamente contenido en la consulta
            return {'total_libros': nodo.total_libros, 
                    'total_prestamos': nodo.total_prestamos}
        
        # Consulta recursiva en ambos hijos
        izquierda = self._consultar_rango(nodo.izquierda, inicio, fin)
        derecha = self._consultar_rango(nodo.derecha, inicio, fin)
        
        # Combina resultados de ambos hijos
        return {
            'total_libros': izquierda['total_libros'] + derecha['total_libros'],
            'total_prestamos': izquierda['total_prestamos'] + derecha['total_prestamos']
        }


# ================= BLOQUE DE PRUEBAS =================

if __name__ == "__main__":
    # Este bloque solo se ejecuta cuando el archivo se corre directamente
    print("=== Prueba de las estructuras de datos ===")
    
    # Prueba de la ListaEnlazada
    lista = ListaEnlazada()
    print(f"Lista inicial: {lista}")
    print(f"¿Está vacía? {lista.esta_vacia()}")
    
    # Agregar elementos
    lista.agregar("Libro 1")
    lista.agregar("Libro 2")
    lista.agregar("Libro 3")
    print(f"Lista después de agregar elementos: {lista}")
    print(f"Tamaño de la lista: {lista.tamanio}")
    
    # Buscar elemento
    resultado = lista.buscar(lambda x: x == "Libro 2")
    print(f"Búsqueda de 'Libro 2': {resultado}")
    
    # Eliminar elemento
    eliminado = lista.eliminar(lambda x: x == "Libro 2")
    print(f"¿Se eliminó 'Libro 2'? {eliminado}")
    print(f"Lista después de eliminar: {lista}")
    print(f"Tamaño de la lista: {lista.tamanio}")
    
    # Listar todos los elementos
    todos = lista.listar()
    print(f"Todos los elementos: {todos}")
    
    print("=== Prueba completada ===")