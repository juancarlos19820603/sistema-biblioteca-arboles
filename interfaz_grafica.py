import tkinter as tk
from tkinter import ttk, messagebox, simpledialog
from tkinter import font as tkfont
import sys
import os
from datetime import datetime

# Importar el sistema de biblioteca desde main.py
from main import obtener_sistema

class BibliotecaApp:
    def __init__(self, root):
        # Inicializar la aplicación principal
        self.root = root
        # Configurar título de la ventana
        self.root.title("Sistema de Gestión de Biblioteca - Con Árboles AVL")
        # Configurar tamaño de la ventana
        self.root.geometry("1200x800")
        # Configurar color de fondo
        self.root.configure(bg='#f5f5f5')
        
        # Inicializar el sistema de biblioteca importado desde main.py
        self.sistema = obtener_sistema()
        
        # Configurar fuentes para la interfaz
        self.title_font = tkfont.Font(family="Helvetica", size=18, weight="bold")
        self.subtitle_font = tkfont.Font(family="Helvetica", size=14, weight="bold")
        self.button_font = tkfont.Font(family="Helvetica", size=10)
        self.text_font = tkfont.Font(family="Helvetica", size=10)
        
        # Variable para mostrar estadísticas dinámicas
        self.stats_text = tk.StringVar()
        
        # Crear el notebook (pestañas) para organizar las diferentes secciones
        self.notebook = ttk.Notebook(root)
        self.notebook.pack(fill='both', expand=True, padx=10, pady=10)
        
        # Crear todas las pestañas de la aplicación
        self.crear_pestana_inicio()
        self.crear_pestana_libros()
        self.crear_pestana_usuarios()
        self.crear_pestana_prestamos()
        self.crear_pestana_reportes()
        self.crear_pestana_busquedas_avanzadas()  # NUEVA PESTAÑA
        
        # Actualizar estadísticas iniciales al cargar la aplicación
        self.actualizar_estadisticas()
    
    def crear_pestana_inicio(self):
        """Crea la pestaña de inicio con estadísticas y acciones rápidas"""
        # Crear frame para la pestaña de inicio
        self.inicio_frame = ttk.Frame(self.notebook)
        self.notebook.add(self.inicio_frame, text="Inicio")
        
        # Título principal de la aplicación
        title_label = tk.Label(self.inicio_frame, text="Sistema de Gestión de Biblioteca con Árboles AVL", 
                              font=self.title_font, bg='#f5f5f5', fg='#2c3e50')
        title_label.pack(pady=30)
        
        # Subtítulo descriptivo
        subtitle_label = tk.Label(self.inicio_frame, text="Sistema optimizado con estructuras de árboles para búsquedas eficientes", 
                                 font=self.subtitle_font, bg='#f5f5f5', fg='#7f8c8d')
        subtitle_label.pack(pady=10)
        
        # Frame para mostrar estadísticas en tiempo real
        stats_frame = tk.LabelFrame(self.inicio_frame, text="Estadísticas en Tiempo Real", font=self.subtitle_font,
                                   bg='#f5f5f5', fg='#2c3e50')
        stats_frame.pack(pady=20, padx=20, fill='x')
        
        # Label que muestra las estadísticas actualizadas
        stats_label = tk.Label(stats_frame, textvariable=self.stats_text, font=self.text_font, 
                              bg='#f5f5f5', justify='left')
        stats_label.pack(pady=10, padx=10)
        
        # Frame para acciones rápidas
        actions_frame = tk.LabelFrame(self.inicio_frame, text="Acciones Rápidas", 
                                     font=self.subtitle_font, bg='#f5f5f5', fg='#2c3e50')
        actions_frame.pack(pady=20, padx=20, fill='x')
        
        # Botones de acciones rápidas
        quick_buttons = [
            ("Agregar Libro", self.agregar_libro),
            ("Registrar Usuario", self.agregar_usuario),
            ("Registrar Préstamo", self.registrar_prestamo),
            ("Búsqueda Avanzada", self.mostrar_busquedas_avanzadas)
        ]
        
        # Crear y empaquetar cada botón de acción rápida
        for text, command in quick_buttons:
            btn = tk.Button(actions_frame, text=text, command=command, 
                          font=self.button_font, bg='#3498db', fg='white',
                          width=20, height=2, relief='flat')
            btn.pack(side='left', padx=10, pady=10)
        
        # Frame para botones de persistencia (guardar/cargar datos)
        persistence_frame = tk.Frame(self.inicio_frame, bg='#f5f5f5')
        persistence_frame.pack(pady=10)
        
        # Botón para guardar datos
        tk.Button(persistence_frame, text="Guardar Datos", command=self.guardar_datos,
                 bg='#27ae60', fg='white', font=self.button_font).pack(side='left', padx=5)
        # Botón para cargar datos
        tk.Button(persistence_frame, text="Cargar Datos", command=self.cargar_datos,
                 bg='#e67e22', fg='white', font=self.button_font).pack(side='left', padx=5)
    
    def crear_pestana_busquedas_avanzadas(self):
        """Crea la pestaña de búsquedas avanzadas utilizando árboles AVL"""
        # Crear frame para la nueva pestaña de búsquedas avanzadas
        self.busquedas_frame = ttk.Frame(self.notebook)
        self.notebook.add(self.busquedas_frame, text="Búsquedas Avanzadas")
        
        # Título de la pestaña
        title_label = tk.Label(self.busquedas_frame, text="Búsquedas Optimizadas con Árboles AVL", 
                              font=self.subtitle_font, bg='#f5f5f5', fg='#2c3e50')
        title_label.pack(pady=20)
        
        # Frame para búsqueda por rango de años
        año_frame = tk.LabelFrame(self.busquedas_frame, text="Búsqueda por Rango de Años", 
                                 font=self.text_font, bg='#f5f5f5')
        año_frame.pack(fill='x', padx=20, pady=10)
        
        # Etiqueta y campo de entrada para año inicio
        tk.Label(año_frame, text="Año inicio:", bg='#f5f5f5').grid(row=0, column=0, padx=5, pady=5)
        self.año_inicio_entry = tk.Entry(año_frame, width=10)
        self.año_inicio_entry.grid(row=0, column=1, padx=5, pady=5)
        
        # Etiqueta y campo de entrada para año fin
        tk.Label(año_frame, text="Año fin:", bg='#f5f5f5').grid(row=0, column=2, padx=5, pady=5)
        self.año_fin_entry = tk.Entry(año_frame, width=10)
        self.año_fin_entry.grid(row=0, column=3, padx=5, pady=5)
        
        # Botón para ejecutar búsqueda por años
        tk.Button(año_frame, text="Buscar por Años", command=self.buscar_por_rango_años,
                 bg='#3498db', fg='white').grid(row=0, column=4, padx=10, pady=5)
        
        # Frame para búsqueda por prefijo
        prefijo_frame = tk.LabelFrame(self.busquedas_frame, text="Búsqueda por Prefijo", 
                                     font=self.text_font, bg='#f5f5f5')
        prefijo_frame.pack(fill='x', padx=20, pady=10)
        
        # Etiqueta y campo de entrada para prefijo
        tk.Label(prefijo_frame, text="Prefijo:", bg='#f5f5f5').grid(row=0, column=0, padx=5, pady=5)
        self.prefijo_entry = tk.Entry(prefijo_frame, width=20)
        self.prefijo_entry.grid(row=0, column=1, padx=5, pady=5)
        
        # Combobox para seleccionar tipo de búsqueda (Título o Autor)
        self.prefijo_tipo = ttk.Combobox(prefijo_frame, values=["Título", "Autor"], width=10)
        self.prefijo_tipo.set("Título")
        self.prefijo_tipo.grid(row=0, column=2, padx=5, pady=5)
        
        # Botón para ejecutar búsqueda por prefijo
        tk.Button(prefijo_frame, text="Buscar por Prefijo", command=self.buscar_por_prefijo,
                 bg='#3498db', fg='white').grid(row=0, column=3, padx=10, pady=5)
        
        # Frame para mostrar resultados de búsqueda
        resultados_frame = tk.Frame(self.busquedas_frame)
        resultados_frame.pack(fill='both', expand=True, padx=20, pady=10)
        
        # Definir columnas para el Treeview de resultados
        columns = ('ISBN', 'Título', 'Autor', 'Año', 'Género', 'Estado')
        self.resultados_tree = ttk.Treeview(resultados_frame, columns=columns, show='headings')
        
        # Configurar encabezados de columnas
        for col in columns:
            self.resultados_tree.heading(col, text=col)
            self.resultados_tree.column(col, width=120)
        
        # Agregar scrollbar para navegar resultados
        scrollbar = ttk.Scrollbar(resultados_frame, orient=tk.VERTICAL, command=self.resultados_tree.yview)
        self.resultados_tree.configure(yscroll=scrollbar.set)
        
        # Empaquetar Treeview y scrollbar
        self.resultados_tree.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
    
    def buscar_por_rango_años(self):
        """Busca libros dentro de un rango de años específico"""
        try:
            # Obtener años desde los campos de entrada
            año_inicio = int(self.año_inicio_entry.get())
            año_fin = int(self.año_fin_entry.get())
            
            # Ejecutar búsqueda en el sistema
            libros = self.sistema.buscar_libros_por_rango_años(año_inicio, año_fin)
            # Mostrar resultados en el Treeview
            self.mostrar_resultados_busqueda(libros)
            
        except ValueError:
            # Mostrar error si los años no son válidos
            messagebox.showerror("Error", "Por favor ingrese años válidos")
    
    def buscar_por_prefijo(self):
        """Busca libros por prefijo en título o autor"""
        # Obtener prefijo y tipo de búsqueda
        prefijo = self.prefijo_entry.get().strip()
        tipo = self.prefijo_tipo.get().lower()
        
        # Validar que se haya ingresado un prefijo
        if not prefijo:
            messagebox.showwarning("Advertencia", "Por favor ingrese un prefijo para buscar")
            return
        
        # Ejecutar búsqueda según el tipo seleccionado
        if tipo == "título":
            libros = self.sistema.buscar_libros_por_titulo(prefijo)
        else:
            libros = self.sistema.buscar_libros_por_autor(prefijo)
        
        # Mostrar resultados
        self.mostrar_resultados_busqueda(libros)
    
    def mostrar_resultados_busqueda(self, libros):
        """Muestra los resultados de búsqueda en el Treeview"""
        # Limpiar resultados anteriores
        for item in self.resultados_tree.get_children():
            self.resultados_tree.delete(item)
        
        # Insertar nuevos resultados
        for libro in libros:
            estado = "Disponible" if libro.disponible else "Prestado"
            self.resultados_tree.insert('', 'end', values=(
                libro.isbn, libro.titulo, libro.autor, 
                libro.año_publicacion, libro.genero, estado
            ))
    
    def actualizar_estadisticas(self):
        """Actualiza las estadísticas mostradas en la pestaña de inicio"""
        # Obtener datos estadísticos del sistema
        total_libros = len(self.sistema.listar_libros())
        libros_disponibles = len(self.sistema.listar_libros_disponibles())
        total_usuarios = len(self.sistema.listar_usuarios())
        prestamos_activos = len(self.sistema.obtener_prestamos_activos())
        
        # Obtener estadísticas de los últimos 10 años
        año_actual = datetime.now().year
        stats_decada = self.sistema.generar_estadisticas_por_año(año_actual - 10, año_actual)
        
        # Construir texto de estadísticas
        stats_text = f"Total de libros: {total_libros}\n"
        stats_text += f"Libros disponibles: {libros_disponibles}\n"
        stats_text += f"Total de usuarios: {total_usuarios}\n"
        stats_text += f"Préstamos activos: {prestamos_activos}\n"
        stats_text += f"Préstamos última década: {stats_decada['total_prestamos']}"
        
        # Actualizar variable de texto
        self.stats_text.set(stats_text)
    
    def guardar_datos(self):
        """Guarda los datos del sistema en archivos"""
        exito, mensaje = self.sistema.guardar_datos()
        if exito:
            messagebox.showinfo("Éxito", mensaje)
        else:
            messagebox.showerror("Error", mensaje)
    
    def cargar_datos(self):
        """Carga los datos del sistema desde archivos"""
        exito, mensaje = self.sistema.cargar_datos()
        if exito:
            messagebox.showinfo("Éxito", mensaje)
            # Actualizar todas las listas y estadísticas
            self.actualizar_lista_libros()
            self.actualizar_lista_usuarios()
            self.actualizar_lista_prestamos()
            self.actualizar_estadisticas()
        else:
            messagebox.showerror("Error", mensaje)

    # MÉTODOS PARA GESTIÓN DE LIBROS
    def crear_pestana_libros(self):
        """Crea la pestaña de gestión de libros"""
        self.libros_frame = ttk.Frame(self.notebook)
        self.notebook.add(self.libros_frame, text="Gestión de Libros")
        
        # Frame para búsqueda de libros
        search_frame = tk.Frame(self.libros_frame, bg='#f5f5f5')
        search_frame.pack(fill='x', padx=10, pady=10)
        
        # Etiqueta y campo de búsqueda
        tk.Label(search_frame, text="Buscar libro:", bg='#f5f5f5').pack(side='left', padx=5)
        self.libro_search_var = tk.StringVar()
        search_entry = tk.Entry(search_frame, textvariable=self.libro_search_var, width=30)
        search_entry.pack(side='left', padx=5)
        
        # Combobox para tipo de búsqueda
        search_type = ttk.Combobox(search_frame, values=["ISBN", "Título", "Autor"], width=10)
        search_type.set("Título")
        search_type.pack(side='left', padx=5)
        
        # Botón de búsqueda
        search_btn = tk.Button(search_frame, text="Buscar", command=lambda: self.buscar_libros(
            self.libro_search_var.get(), search_type.get()), bg='#3498db', fg='white')
        search_btn.pack(side='left', padx=5)
        
        # Frame para lista de libros
        list_frame = tk.Frame(self.libros_frame)
        list_frame.pack(fill='both', expand=True, padx=10, pady=10)
        
        # Treeview para mostrar libros
        columns = ('ISBN', 'Título', 'Autor', 'Año', 'Género', 'Estado')
        self.libros_tree = ttk.Treeview(list_frame, columns=columns, show='headings')
        
        # Configurar columnas
        for col in columns:
            self.libros_tree.heading(col, text=col)
            self.libros_tree.column(col, width=120)
        
        # Scrollbar para la lista
        scrollbar = ttk.Scrollbar(list_frame, orient=tk.VERTICAL, command=self.libros_tree.yview)
        self.libros_tree.configure(yscroll=scrollbar.set)
        
        self.libros_tree.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        
        # Frame para botones de acción
        action_frame = tk.Frame(self.libros_frame, bg='#f5f5f5')
        action_frame.pack(fill='x', padx=10, pady=10)
        
        # Botones de acción para libros
        action_buttons = [
            ("Agregar Libro", self.agregar_libro),
            ("Editar Libro", self.editar_libro),
            ("Eliminar Libro", self.eliminar_libro),
            ("Actualizar Lista", self.actualizar_lista_libros)
        ]
        
        # Crear y empaquetar botones
        for text, command in action_buttons:
            btn = tk.Button(action_frame, text=text, command=command, 
                          font=self.button_font, bg='#3498db', fg='white',
                          width=15, height=1, relief='flat')
            btn.pack(side='left', padx=5, pady=5)
        
        # Cargar lista inicial de libros
        self.actualizar_lista_libros()
    
    def actualizar_lista_libros(self):
        """Actualiza la lista de libros en el Treeview"""
        # Limpiar lista actual
        for item in self.libros_tree.get_children():
            self.libros_tree.delete(item)
        
        # Obtener y mostrar todos los libros
        libros = self.sistema.listar_libros()
        for libro in libros:
            estado = "Disponible" if libro.disponible else "Prestado"
            self.libros_tree.insert('', 'end', values=(
                libro.isbn, libro.titulo, libro.autor, libro.año_publicacion, 
                libro.genero, estado
            ))
    
    def buscar_libros(self, criterio, tipo):
        """Busca libros según criterio y tipo especificado"""
        # Limpiar lista actual
        for item in self.libros_tree.get_children():
            self.libros_tree.delete(item)
        
        # Buscar según el tipo seleccionado
        if tipo == "ISBN":
            libro = self.sistema.buscar_libro_por_isbn(criterio)
            if libro:
                estado = "Disponible" if libro.disponible else "Prestado"
                self.libros_tree.insert('', 'end', values=(
                    libro.isbn, libro.titulo, libro.autor, libro.año_publicacion, 
                    libro.genero, estado
                ))
        elif tipo == "Título":
            libros = self.sistema.buscar_libros_por_titulo(criterio)
            for libro in libros:
                estado = "Disponible" if libro.disponible else "Prestado"
                self.libros_tree.insert('', 'end', values=(
                    libro.isbn, libro.titulo, libro.autor, libro.año_publicacion, 
                    libro.genero, estado
                ))
        elif tipo == "Autor":
            libros = self.sistema.buscar_libros_por_autor(criterio)
            for libro in libros:
                estado = "Disponible" if libro.disponible else "Prestado"
                self.libros_tree.insert('', 'end', values=(
                    libro.isbn, libro.titulo, libro.autor, libro.año_publicacion, 
                    libro.genero, estado
                ))
    
    def agregar_libro(self):
        """Abre ventana para agregar un nuevo libro"""
        add_window = tk.Toplevel(self.root)
        add_window.title("Agregar Libro")
        add_window.geometry("500x400")
        add_window.configure(bg='#f5f5f5')
        add_window.grab_set()  # Hacer ventana modal
        
        main_frame = tk.Frame(add_window, bg='#f5f5f5')
        main_frame.pack(expand=True, fill='both', padx=20, pady=20)
        
        title_label = tk.Label(main_frame, text="Agregar Nuevo Libro", 
                              font=self.subtitle_font, bg='#f5f5f5', fg='#2c3e50')
        title_label.pack(pady=10)
        
        form_frame = tk.Frame(main_frame, bg='#f5f5f5')
        form_frame.pack(pady=20)
        
        # Campos del formulario
        fields = [
            ("ISBN:", "isbn"),
            ("Título:", "titulo"),
            ("Autor:", "autor"),
            ("Año de publicación:", "año"),
            ("Género:", "genero")
        ]
        
        self.entries = {}
        for i, (label, field) in enumerate(fields):
            lbl = tk.Label(form_frame, text=label, bg='#f5f5f5', anchor='e', width=15)
            lbl.grid(row=i, column=0, sticky='e', padx=5, pady=5)
            entry = tk.Entry(form_frame, width=30)
            entry.grid(row=i, column=1, padx=5, pady=5)
            self.entries[field] = entry
        
        button_frame = tk.Frame(main_frame, bg='#f5f5f5')
        button_frame.pack(pady=20)
        
        def guardar_libro():
            """Función interna para guardar el libro"""
            datos = {field: self.entries[field].get() for field in self.entries}
            
            # Validar campos obligatorios
            if not all([datos['isbn'], datos['titulo'], datos['autor']]):
                messagebox.showerror("Error", "ISBN, Título y Autor son campos obligatorios")
                return
            
            # Validar año
            try:
                año = int(datos['año']) if datos['año'] else 0
            except ValueError:
                messagebox.showerror("Error", "El año debe ser un número válido")
                return
            
            # Agregar libro al sistema
            exito, mensaje = self.sistema.agregar_libro(
                datos['isbn'], datos['titulo'], datos['autor'], año, datos['genero']
            )
            
            if exito:
                messagebox.showinfo("Éxito", mensaje)
                add_window.destroy()
                self.actualizar_lista_libros()
                self.actualizar_estadisticas()
            else:
                messagebox.showerror("Error", mensaje)
        
        # Botones de guardar y cancelar
        tk.Button(button_frame, text="Guardar", command=guardar_libro,
                 bg='#27ae60', fg='white', font=self.button_font).pack(side='left', padx=10)
        tk.Button(button_frame, text="Cancelar", command=add_window.destroy,
                 bg='#e74c3c', fg='white', font=self.button_font).pack(side='left', padx=10)

    # MÉTODOS PARA EDITAR Y ELIMINAR LIBROS
    def editar_libro(self):
        """Abre ventana para editar un libro existente"""
        selected_item = self.libros_tree.selection()
        if not selected_item:
            messagebox.showwarning("Advertencia", "Por favor seleccione un libro para editar")
            return
        
        # Obtener ISBN del libro seleccionado
        isbn = self.libros_tree.item(selected_item[0])['values'][0]
        libro = self.sistema.buscar_libro_por_isbn(isbn)
        if not libro:
            messagebox.showerror("Error", "No se encontró el libro seleccionado")
            return
        
        # Crear ventana de edición
        edit_window = tk.Toplevel(self.root)
        edit_window.title("Editar Libro")
        edit_window.geometry("500x400")
        edit_window.configure(bg='#f5f5f5')
        edit_window.grab_set()
        
        main_frame = tk.Frame(edit_window, bg='#f5f5f5')
        main_frame.pack(expand=True, fill='both', padx=20, pady=20)
        
        title_label = tk.Label(main_frame, text="Editar Libro", 
                              font=self.subtitle_font, bg='#f5f5f5', fg='#2c3e50')
        title_label.pack(pady=10)
        
        form_frame = tk.Frame(main_frame, bg='#f5f5f5')
        form_frame.pack(pady=20)
        
        # Campos del formulario con valores actuales
        fields = [
            ("ISBN:", "isbn", libro.isbn, False),
            ("Título:", "titulo", libro.titulo, True),
            ("Autor:", "autor", libro.autor, True),
            ("Año de publicación:", "año", libro.año_publicacion, True),
            ("Género:", "genero", libro.genero, True)
        ]
        
        self.edit_entries = {}
        for i, (label, field, value, editable) in enumerate(fields):
            lbl = tk.Label(form_frame, text=label, bg='#f5f5f5', anchor='e', width=15)
            lbl.grid(row=i, column=0, sticky='e', padx=5, pady=5)
            entry = tk.Entry(form_frame, width=30)
            entry.insert(0, str(value))
            if not editable:
                entry.config(state='readonly')
            entry.grid(row=i, column=1, padx=5, pady=5)
            self.edit_entries[field] = entry
        
        button_frame = tk.Frame(main_frame, bg='#f5f5f5')
        button_frame.pack(pady=20)
        
        def actualizar_libro():
            """Función interna para actualizar el libro"""
            nuevos_datos = {}
            for field in self.edit_entries:
                if field != 'isbn':
                    nuevos_datos[field] = self.edit_entries[field].get()
            
            # Validar año
            try:
                if 'año' in nuevos_datos:
                    nuevos_datos['año'] = int(nuevos_datos['año'])
            except ValueError:
                messagebox.showerror("Error", "El año debe ser un número válido")
                return
            
            # Actualizar libro en el sistema
            exito, mensaje = self.sistema.actualizar_libro(isbn, nuevos_datos)
            
            if exito:
                messagebox.showinfo("Éxito", mensaje)
                edit_window.destroy()
                self.actualizar_lista_libros()
                self.actualizar_estadisticas()
            else:
                messagebox.showerror("Error", mensaje)
        
        # Botones de actualizar y cancelar
        tk.Button(button_frame, text="Actualizar", command=actualizar_libro,
                 bg='#27ae60', fg='white', font=self.button_font).pack(side='left', padx=10)
        tk.Button(button_frame, text="Cancelar", command=edit_window.destroy,
                 bg='#e74c3c', fg='white', font=self.button_font).pack(side='left', padx=10)
    
    def eliminar_libro(self):
        """Elimina un libro seleccionado"""
        selected_item = self.libros_tree.selection()
        if not selected_item:
            messagebox.showwarning("Advertencia", "Por favor seleccione un libro para eliminar")
            return
        
        # Obtener datos del libro seleccionado
        isbn = self.libros_tree.item(selected_item[0])['values'][0]
        titulo = self.libros_tree.item(selected_item[0])['values'][1]
        
        # Confirmar eliminación
        confirmar = messagebox.askyesno(
            "Confirmar eliminación", 
            f"¿Está seguro de que desea eliminar el libro '{titulo}' (ISBN: {isbn})?"
        )
        
        if confirmar:
            # Eliminar libro del sistema
            exito, mensaje = self.sistema.eliminar_libro(isbn)
            
            if exito:
                messagebox.showinfo("Éxito", mensaje)
                self.actualizar_lista_libros()
                self.actualizar_estadisticas()
            else:
                messagebox.showerror("Error", mensaje)
    
    # MÉTODOS PARA GESTIÓN DE USUARIOS
    def crear_pestana_usuarios(self):
        """Crea la pestaña de gestión de usuarios"""
        self.usuarios_frame = ttk.Frame(self.notebook)
        self.notebook.add(self.usuarios_frame, text="Gestión de Usuarios")
        
        # Frame para búsqueda de usuarios
        search_frame = tk.Frame(self.usuarios_frame, bg='#f5f5f5')
        search_frame.pack(fill='x', padx=10, pady=10)
        
        tk.Label(search_frame, text="Buscar usuario:", bg='#f5f5f5').pack(side='left', padx=5)
        self.usuario_search_var = tk.StringVar()
        search_entry = tk.Entry(search_frame, textvariable=self.usuario_search_var, width=30)
        search_entry.pack(side='left', padx=5)
        
        search_type = ttk.Combobox(search_frame, values=["ID", "Nombre"], width=10)
        search_type.set("Nombre")
        search_type.pack(side='left', padx=5)
        
        search_btn = tk.Button(search_frame, text="Buscar", command=lambda: self.buscar_usuarios(
            self.usuario_search_var.get(), search_type.get()), bg='#3498db', fg='white')
        search_btn.pack(side='left', padx=5)
        
        # Frame para lista de usuarios
        list_frame = tk.Frame(self.usuarios_frame)
        list_frame.pack(fill='both', expand=True, padx=10, pady=10)
        
        # Treeview para mostrar usuarios
        columns = ('ID', 'Nombre', 'Contacto')
        self.usuarios_tree = ttk.Treeview(list_frame, columns=columns, show='headings')
        
        for col in columns:
            self.usuarios_tree.heading(col, text=col)
            self.usuarios_tree.column(col, width=150)
        
        # Scrollbar para la lista
        scrollbar = ttk.Scrollbar(list_frame, orient=tk.VERTICAL, command=self.usuarios_tree.yview)
        self.usuarios_tree.configure(yscroll=scrollbar.set)
        
        self.usuarios_tree.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        
        # Frame para botones de acción
        action_frame = tk.Frame(self.usuarios_frame, bg='#f5f5f5')
        action_frame.pack(fill='x', padx=10, pady=10)
        
        # Botones de acción para usuarios
        action_buttons = [
            ("Agregar Usuario", self.agregar_usuario),
            ("Editar Usuario", self.editar_usuario),
            ("Eliminar Usuario", self.eliminar_usuario),
            ("Actualizar Lista", self.actualizar_lista_usuarios)
        ]
        
        for text, command in action_buttons:
            btn = tk.Button(action_frame, text=text, command=command, 
                          font=self.button_font, bg='#3498db', fg='white',
                          width=15, height=1, relief='flat')
            btn.pack(side='left', padx=5, pady=5)
        
        # Cargar lista inicial de usuarios
        self.actualizar_lista_usuarios()
    
    def actualizar_lista_usuarios(self):
        """Actualiza la lista de usuarios en el Treeview"""
        for item in self.usuarios_tree.get_children():
            self.usuarios_tree.delete(item)
        
        usuarios = self.sistema.listar_usuarios()
        for usuario in usuarios:
            self.usuarios_tree.insert('', 'end', values=(
                usuario.id_usuario, usuario.nombre, usuario.contacto
            ))
    
    def buscar_usuarios(self, criterio, tipo):
        """Busca usuarios según criterio y tipo especificado"""
        for item in self.usuarios_tree.get_children():
            self.usuarios_tree.delete(item)
        
        if tipo == "ID":
            usuario = self.sistema.buscar_usuario_por_id(criterio)
            if usuario:
                self.usuarios_tree.insert('', 'end', values=(
                    usuario.id_usuario, usuario.nombre, usuario.contacto
                ))
        elif tipo == "Nombre":
            usuarios = self.sistema.buscar_usuarios_por_nombre(criterio)
            for usuario in usuarios:
                self.usuarios_tree.insert('', 'end', values=(
                    usuario.id_usuario, usuario.nombre, usuario.contacto
                ))
    
    def agregar_usuario(self):
        """Abre ventana para agregar un nuevo usuario"""
        add_window = tk.Toplevel(self.root)
        add_window.title("Agregar Usuario")
        add_window.geometry("500x300")
        add_window.configure(bg='#f5f5f5')
        add_window.grab_set()
        
        main_frame = tk.Frame(add_window, bg='#f5f5f5')
        main_frame.pack(expand=True, fill='both', padx=20, pady=20)
        
        title_label = tk.Label(main_frame, text="Agregar Nuevo Usuario", 
                              font=self.subtitle_font, bg='#f5f5f5', fg='#2c3e50')
        title_label.pack(pady=10)
        
        form_frame = tk.Frame(main_frame, bg='#f5f5f5')
        form_frame.pack(pady=20)
        
        # Campos del formulario
        fields = [
            ("ID de usuario:", "id_usuario"),
            ("Nombre:", "nombre"),
            ("Contacto:", "contacto")
        ]
        
        self.user_entries = {}
        for i, (label, field) in enumerate(fields):
            lbl = tk.Label(form_frame, text=label, bg='#f5f5f5', anchor='e', width=15)
            lbl.grid(row=i, column=0, sticky='e', padx=5, pady=5)
            entry = tk.Entry(form_frame, width=30)
            entry.grid(row=i, column=1, padx=5, pady=5)
            self.user_entries[field] = entry
        
        button_frame = tk.Frame(main_frame, bg='#f5f5f5')
        button_frame.pack(pady=20)
        
        def guardar_usuario():
            """Función interna para guardar el usuario"""
            datos = {field: self.user_entries[field].get() for field in self.user_entries}
            
            # Validar campos obligatorios
            if not all([datos['id_usuario'], datos['nombre']]):
                messagebox.showerror("Error", "ID y Nombre son campos obligatorios")
                return
            
            # Agregar usuario al sistema
            exito, mensaje = self.sistema.agregar_usuario(
                datos['id_usuario'], datos['nombre'], datos['contacto']
            )
            
            if exito:
                messagebox.showinfo("Éxito", mensaje)
                add_window.destroy()
                self.actualizar_lista_usuarios()
                self.actualizar_estadisticas()
            else:
                messagebox.showerror("Error", mensaje)
        
        # Botones de guardar y cancelar
        tk.Button(button_frame, text="Guardar", command=guardar_usuario,
                 bg='#27ae60', fg='white', font=self.button_font).pack(side='left', padx=10)
        tk.Button(button_frame, text="Cancelar", command=add_window.destroy,
                 bg='#e74c3c', fg='white', font=self.button_font).pack(side='left', padx=10)
    
    def editar_usuario(self):
        """Abre ventana para editar un usuario existente"""
        selected_item = self.usuarios_tree.selection()
        if not selected_item:
            messagebox.showwarning("Advertencia", "Por favor seleccione un usuario para editar")
            return
        
        # Obtener ID del usuario seleccionado
        id_usuario = self.usuarios_tree.item(selected_item[0])['values'][0]
        usuario = self.sistema.buscar_usuario_por_id(id_usuario)
        if not usuario:
            messagebox.showerror("Error", "No se encontró el usuario seleccionado")
            return
        
        # Crear ventana de edición
        edit_window = tk.Toplevel(self.root)
        edit_window.title("Editar Usuario")
        edit_window.geometry("500x300")
        edit_window.configure(bg='#f5f5f5')
        edit_window.grab_set()
        
        main_frame = tk.Frame(edit_window, bg='#f5f5f5')
        main_frame.pack(expand=True, fill='both', padx=20, pady=20)
        
        title_label = tk.Label(main_frame, text="Editar Usuario", 
                              font=self.subtitle_font, bg='#f5f5f5', fg='#2c3e50')
        title_label.pack(pady=10)
        
        form_frame = tk.Frame(main_frame, bg='#f5f5f5')
        form_frame.pack(pady=20)
        
        # Campos del formulario con valores actuales
        fields = [
            ("ID de usuario:", "id_usuario", usuario.id_usuario, False),
            ("Nombre:", "nombre", usuario.nombre, True),
            ("Contacto:", "contacto", usuario.contacto, True)
        ]
        
        self.edit_user_entries = {}
        for i, (label, field, value, editable) in enumerate(fields):
            lbl = tk.Label(form_frame, text=label, bg='#f5f5f5', anchor='e', width=15)
            lbl.grid(row=i, column=0, sticky='e', padx=5, pady=5)
            entry = tk.Entry(form_frame, width=30)
            entry.insert(0, str(value))
            if not editable:
                entry.config(state='readonly')
            entry.grid(row=i, column=1, padx=5, pady=5)
            self.edit_user_entries[field] = entry
        
        button_frame = tk.Frame(main_frame, bg='#f5f5f5')
        button_frame.pack(pady=20)
        
        def actualizar_usuario():
            """Función interna para actualizar el usuario"""
            nuevos_datos = {}
            for field in self.edit_user_entries:
                if field != 'id_usuario':
                    nuevos_datos[field] = self.edit_user_entries[field].get()
            
            # Actualizar usuario en el sistema
            exito, mensaje = self.sistema.actualizar_usuario(id_usuario, nuevos_datos)
            
            if exito:
                messagebox.showinfo("Éxito", mensaje)
                edit_window.destroy()
                self.actualizar_lista_usuarios()
                self.actualizar_estadisticas()
            else:
                messagebox.showerror("Error", mensaje)
        
        # Botones de actualizar y cancelar
        tk.Button(button_frame, text="Actualizar", command=actualizar_usuario,
                 bg='#27ae60', fg='white', font=self.button_font).pack(side='left', padx=10)
        tk.Button(button_frame, text="Cancelar", command=edit_window.destroy,
                 bg='#e74c3c', fg='white', font=self.button_font).pack(side='left', padx=10)
    
    def eliminar_usuario(self):
        """Elimina un usuario seleccionado"""
        selected_item = self.usuarios_tree.selection()
        if not selected_item:
            messagebox.showwarning("Advertencia", "Por favor seleccione un usuario para eliminar")
            return
        
        # Obtener datos del usuario seleccionado
        id_usuario = self.usuarios_tree.item(selected_item[0])['values'][0]
        nombre = self.usuarios_tree.item(selected_item[0])['values'][1]
        
        # Confirmar eliminación
        confirmar = messagebox.askyesno(
            "Confirmar eliminación", 
            f"¿Está seguro de que desea eliminar al usuario '{nombre}' (ID: {id_usuario})?"
        )
        
        if confirmar:
            # Eliminar usuario del sistema
            exito, mensaje = self.sistema.eliminar_usuario(id_usuario)
            
            if exito:
                messagebox.showinfo("Éxito", mensaje)
                self.actualizar_lista_usuarios()
                self.actualizar_estadisticas()
            else:
                messagebox.showerror("Error", mensaje)
    
    # MÉTODOS PARA GESTIÓN DE PRÉSTAMOS
    def crear_pestana_prestamos(self):
        """Crea la pestaña de gestión de préstamos"""
        self.prestamos_frame = ttk.Frame(self.notebook)
        self.notebook.add(self.prestamos_frame, text="Gestión de Préstamos")
        
        # Frame para operaciones de préstamos
        operations_frame = tk.LabelFrame(self.prestamos_frame, text="Operaciones de Préstamos", 
                                       font=self.subtitle_font, bg='#f5f5f5', fg='#2c3e50')
        operations_frame.pack(fill='x', padx=10, pady=10)
        
        # Botones de operaciones
        operation_buttons = [
            ("Registrar Préstamo", self.registrar_prestamo),
            ("Registrar Devolución", self.registrar_devolucion),
            ("Actualizar Lista", self.actualizar_lista_prestamos)
        ]
        
        for text, command in operation_buttons:
            btn = tk.Button(operations_frame, text=text, command=command, 
                          font=self.button_font, bg='#3498db', fg='white',
                          width=15, height=2, relief='flat')
            btn.pack(side='left', padx=10, pady=10)
        
        # Frame para lista de préstamos
        list_frame = tk.Frame(self.prestamos_frame)
        list_frame.pack(fill='both', expand=True, padx=10, pady=10)
        
        # Treeview para mostrar préstamos
        columns = ('ID Préstamo', 'ISBN Libro', 'ID Usuario', 'Fecha Préstamo', 'Fecha Devolución', 'Estado')
        self.prestamos_tree = ttk.Treeview(list_frame, columns=columns, show='headings')
        
        # Configurar anchos de columnas
        column_widths = [100, 120, 100, 120, 120, 100]
        for i, col in enumerate(columns):
            self.prestamos_tree.heading(col, text=col)
            self.prestamos_tree.column(col, width=column_widths[i])
        
        # Scrollbar para la lista
        scrollbar = ttk.Scrollbar(list_frame, orient=tk.VERTICAL, command=self.prestamos_tree.yview)
        self.prestamos_tree.configure(yscroll=scrollbar.set)
        
        self.prestamos_tree.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        
        # Cargar lista inicial de préstamos
        self.actualizar_lista_prestamos()
    
    def actualizar_lista_prestamos(self):
        """Actualiza la lista de préstamos en el Treeview"""
        for item in self.prestamos_tree.get_children():
            self.prestamos_tree.delete(item)
        
        prestamos = self.sistema.listar_todos_los_prestamos()
        for prestamo in prestamos:
            estado = "Activo" if prestamo.activo else "Finalizado"
            self.prestamos_tree.insert('', 'end', values=(
                prestamo.id_prestamo, prestamo.isbn_libro, prestamo.id_usuario,
                prestamo.fecha_prestamo, prestamo.fecha_devolucion or "No devuelto", estado
            ))
    
    def registrar_prestamo(self):
        """Abre ventana para registrar un nuevo préstamo"""
        prestamo_window = tk.Toplevel(self.root)
        prestamo_window.title("Registrar Préstamo")
        prestamo_window.geometry("500x300")
        prestamo_window.configure(bg='#f5f5f5')
        prestamo_window.grab_set()
        
        main_frame = tk.Frame(prestamo_window, bg='#f5f5f5')
        main_frame.pack(expand=True, fill='both', padx=20, pady=20)
        
        title_label = tk.Label(main_frame, text="Registrar Nuevo Préstamo", 
                              font=self.subtitle_font, bg='#f5f5f5', fg='#2c3e50')
        title_label.pack(pady=10)
        
        form_frame = tk.Frame(main_frame, bg='#f5f5f5')
        form_frame.pack(pady=20)
        
        # Campos del formulario
        fields = [
            ("ISBN del libro:", "isbn_libro"),
            ("ID del usuario:", "id_usuario"),
            ("Fecha de préstamo (YYYY-MM-DD):", "fecha_prestamo")
        ]
        
        self.prestamo_entries = {}
        for i, (label, field) in enumerate(fields):
            lbl = tk.Label(form_frame, text=label, bg='#f5f5f5', anchor='e', width=25)
            lbl.grid(row=i, column=0, sticky='e', padx=5, pady=5)
            entry = tk.Entry(form_frame, width=30)
            entry.grid(row=i, column=1, padx=5, pady=5)
            self.prestamo_entries[field] = entry
        
        button_frame = tk.Frame(main_frame, bg='#f5f5f5')
        button_frame.pack(pady=20)
        
        def guardar_prestamo():
            """Función interna para guardar el préstamo"""
            datos = {field: self.prestamo_entries[field].get() for field in self.prestamo_entries}
            
            # Validar campos obligatorios
            if not all(datos.values()):
                messagebox.showerror("Error", "Todos los campos son obligatorios")
                return
            
            # Registrar préstamo en el sistema
            exito, mensaje = self.sistema.registrar_prestamo(
                datos['isbn_libro'], datos['id_usuario'], datos['fecha_prestamo']
            )
            
            if exito:
                messagebox.showinfo("Éxito", mensaje)
                prestamo_window.destroy()
                self.actualizar_lista_prestamos()
                self.actualizar_lista_libros()
                self.actualizar_estadisticas()
            else:
                messagebox.showerror("Error", mensaje)
        
        # Botones de registrar y cancelar
        tk.Button(button_frame, text="Registrar", command=guardar_prestamo,
                 bg='#27ae60', fg='white', font=self.button_font).pack(side='left', padx=10)
        tk.Button(button_frame, text="Cancelar", command=prestamo_window.destroy,
                 bg='#e74c3c', fg='white', font=self.button_font).pack(side='left', padx=10)
    
    def registrar_devolucion(self):
        """Registra la devolución de un préstamo seleccionado"""
        selected_item = self.prestamos_tree.selection()
        if not selected_item:
            messagebox.showwarning("Advertencia", "Por favor seleccione un préstamo para registrar devolución")
            return
        
        # Obtener datos del préstamo seleccionado
        id_prestamo = self.prestamos_tree.item(selected_item[0])['values'][0]
        estado = self.prestamos_tree.item(selected_item[0])['values'][5]
        
        # Validar que el préstamo esté activo
        if estado != "Activo":
            messagebox.showwarning("Advertencia", "Solo se pueden registrar devoluciones de préstamos activos")
            return
        
        # Solicitar fecha de devolución
        fecha_devolucion = simpledialog.askstring(
            "Registrar Devolución", 
            f"Ingrese la fecha de devolución (YYYY-MM-DD) para el préstamo {id_prestamo}:"
        )
        
        if fecha_devolucion:
            # Registrar devolución en el sistema
            exito, mensaje = self.sistema.registrar_devolucion(id_prestamo, fecha_devolucion)
            
            if exito:
                messagebox.showinfo("Éxito", mensaje)
                self.actualizar_lista_prestamos()
                self.actualizar_lista_libros()
                self.actualizar_estadisticas()
            else:
                messagebox.showerror("Error", mensaje)
    
    # MÉTODOS PARA REPORTES
    def crear_pestana_reportes(self):
        """Crea la pestaña de reportes del sistema"""
        self.reportes_frame = ttk.Frame(self.notebook)
        self.notebook.add(self.reportes_frame, text="Reportes")
        
        reports_frame = tk.Frame(self.reportes_frame, bg='#f5f5f5')
        reports_frame.pack(fill='both', expand=True, padx=10, pady=10)
        
        title_label = tk.Label(reports_frame, text="Reportes del Sistema", 
                              font=self.subtitle_font, bg='#f5f5f5', fg='#2c3e50')
        title_label.pack(pady=10)
        
        buttons_frame = tk.Frame(reports_frame, bg='#f5f5f5')
        buttons_frame.pack(pady=20)
        
        # Botones para diferentes tipos de reportes
        report_buttons = [
            ("Libros Disponibles", self.mostrar_libros_disponibles),
            ("Préstamos Activos", self.mostrar_prestamos_activos),
            ("Todos los Libros", self.mostrar_todos_libros),
            ("Todos los Usuarios", self.mostrar_todos_usuarios),
            ("Libros Más Antiguos", self.mostrar_libros_antiguos),
            ("Estadísticas por Años", self.mostrar_estadisticas_años)
        ]
        
        # Crear botones en una cuadrícula 2x3
        for i, (text, command) in enumerate(report_buttons):
            btn = tk.Button(buttons_frame, text=text, command=command, 
                          font=self.button_font, bg='#3498db', fg='white',
                          width=20, height=2, relief='flat')
            btn.grid(row=i//2, column=i%2, padx=10, pady=10)
    
    def mostrar_libros_disponibles(self):
        """Muestra ventana con reporte de libros disponibles"""
        disp_window = tk.Toplevel(self.root)
        disp_window.title("Libros Disponibles")
        disp_window.geometry("800x400")
        
        main_frame = tk.Frame(disp_window)
        main_frame.pack(fill='both', expand=True, padx=10, pady=10)
        
        title_label = tk.Label(main_frame, text="Libros Disponibles", 
                              font=self.subtitle_font)
        title_label.pack(pady=10)
        
        # Treeview para mostrar libros disponibles
        columns = ('ISBN', 'Título', 'Autor', 'Año', 'Género')
        tree = ttk.Treeview(main_frame, columns=columns, show='headings')
        
        for col in columns:
            tree.heading(col, text=col)
            tree.column(col, width=120)
        
        scrollbar = ttk.Scrollbar(main_frame, orient=tk.VERTICAL, command=tree.yview)
        tree.configure(yscroll=scrollbar.set)
        
        tree.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        
        # Obtener y mostrar libros disponibles
        libros = self.sistema.listar_libros_disponibles()
        for libro in libros:
            tree.insert('', 'end', values=(
                libro.isbn, libro.titulo, libro.autor, 
                libro.año_publicacion, libro.genero
            ))
    
    def mostrar_prestamos_activos(self):
        """Muestra ventana con reporte de préstamos activos"""
        activos_window = tk.Toplevel(self.root)
        activos_window.title("Préstamos Activos")
        activos_window.geometry("900x400")
        
        main_frame = tk.Frame(activos_window)
        main_frame.pack(fill='both', expand=True, padx=10, pady=10)
        
        title_label = tk.Label(main_frame, text="Préstamos Activos", 
                              font=self.subtitle_font)
        title_label.pack(pady=10)
        
        # Treeview para mostrar préstamos activos
        columns = ('ID Préstamo', 'ISBN Libro', 'ID Usuario', 'Fecha Préstamo')
        tree = ttk.Treeview(main_frame, columns=columns, show='headings')
        
        column_widths = [100, 120, 100, 120]
        for i, col in enumerate(columns):
            tree.heading(col, text=col)
            tree.column(col, width=column_widths[i])
        
        scrollbar = ttk.Scrollbar(main_frame, orient=tk.VERTICAL, command=tree.yview)
        tree.configure(yscroll=scrollbar.set)
        
        tree.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        
        # Obtener y mostrar préstamos activos
        prestamos = self.sistema.obtener_prestamos_activos()
        for prestamo in prestamos:
            tree.insert('', 'end', values=(
                prestamo.id_prestamo, prestamo.isbn_libro, 
                prestamo.id_usuario, prestamo.fecha_prestamo
            ))
    
    def mostrar_todos_libros(self):
        """Muestra ventana con reporte de todos los libros"""
        all_window = tk.Toplevel(self.root)
        all_window.title("Todos los Libros")
        all_window.geometry("800x400")
        
        main_frame = tk.Frame(all_window)
        main_frame.pack(fill='both', expand=True, padx=10, pady=10)
        
        title_label = tk.Label(main_frame, text="Todos los Libros", 
                              font=self.subtitle_font)
        title_label.pack(pady=10)
        
        # Treeview para mostrar todos los libros
        columns = ('ISBN', 'Título', 'Autor', 'Año', 'Género', 'Estado')
        tree = ttk.Treeview(main_frame, columns=columns, show='headings')
        
        for col in columns:
            tree.heading(col, text=col)
            tree.column(col, width=120)
        
        scrollbar = ttk.Scrollbar(main_frame, orient=tk.VERTICAL, command=tree.yview)
        tree.configure(yscroll=scrollbar.set)
        
        tree.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        
        # Obtener y mostrar todos los libros
        libros = self.sistema.listar_libros()
        for libro in libros:
            estado = "Disponible" if libro.disponible else "Prestado"
            tree.insert('', 'end', values=(
                libro.isbn, libro.titulo, libro.autor, 
                libro.año_publicacion, libro.genero, estado
            ))
    
    def mostrar_todos_usuarios(self):
        """Muestra ventana con reporte de todos los usuarios"""
        users_window = tk.Toplevel(self.root)
        users_window.title("Todos los Usuarios")
        users_window.geometry("700x400")
        
        main_frame = tk.Frame(users_window)
        main_frame.pack(fill='both', expand=True, padx=10, pady=10)
        
        title_label = tk.Label(main_frame, text="Todos los Usuarios", 
                              font=self.subtitle_font)
        title_label.pack(pady=10)
        
        # Treeview para mostrar todos los usuarios
        columns = ('ID', 'Nombre', 'Contacto')
        tree = ttk.Treeview(main_frame, columns=columns, show='headings')
        
        for col in columns:
            tree.heading(col, text=col)
            tree.column(col, width=150)
        
        scrollbar = ttk.Scrollbar(main_frame, orient=tk.VERTICAL, command=tree.yview)
        tree.configure(yscroll=scrollbar.set)
        
        tree.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        
        # Obtener y mostrar todos los usuarios
        usuarios = self.sistema.listar_usuarios()
        for usuario in usuarios:
            tree.insert('', 'end', values=(
                usuario.id_usuario, usuario.nombre, usuario.contacto
            ))
    
    def mostrar_libros_antiguos(self):
        """Muestra ventana con reporte de libros más antiguos"""
        antiguos_window = tk.Toplevel(self.root)
        antiguos_window.title("Libros Más Antiguos")
        antiguos_window.geometry("800x400")
        
        main_frame = tk.Frame(antiguos_window)
        main_frame.pack(fill='both', expand=True, padx=10, pady=10)
        
        title_label = tk.Label(main_frame, text="Libros Más Antiguos", 
                              font=self.subtitle_font)
        title_label.pack(pady=10)
        
        # Treeview para mostrar libros antiguos
        columns = ('ISBN', 'Título', 'Autor', 'Año', 'Género')
        tree = ttk.Treeview(main_frame, columns=columns, show='headings')
        
        for col in columns:
            tree.heading(col, text=col)
            tree.column(col, width=120)
        
        scrollbar = ttk.Scrollbar(main_frame, orient=tk.VERTICAL, command=tree.yview)
        tree.configure(yscroll=scrollbar.set)
        
        tree.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        
        # Obtener y mostrar libros más antiguos
        libros_antiguos = self.sistema.obtener_libros_mas_antiguos(10)
        for libro in libros_antiguos:
            tree.insert('', 'end', values=(
                libro.isbn, libro.titulo, libro.autor, 
                libro.año_publicacion, libro.genero
            ))
    
    def mostrar_estadisticas_años(self):
        """Muestra ventana con estadísticas por rango de años"""
        stats_window = tk.Toplevel(self.root)
        stats_window.title("Estadísticas por Años")
        stats_window.geometry("600x400")
        
        main_frame = tk.Frame(stats_window)
        main_frame.pack(fill='both', expand=True, padx=10, pady=10)
        
        title_label = tk.Label(main_frame, text="Estadísticas por Rango de Años", 
                              font=self.subtitle_font)
        title_label.pack(pady=10)
        
        # Frame para entrada de años
        input_frame = tk.Frame(main_frame)
        input_frame.pack(pady=10)
        
        # Campos para año inicio y año fin
        tk.Label(input_frame, text="Año inicio:").grid(row=0, column=0, padx=5, pady=5)
        año_inicio_entry = tk.Entry(input_frame, width=10)
        año_inicio_entry.grid(row=0, column=1, padx=5, pady=5)
        año_inicio_entry.insert(0, "1900")
        
        tk.Label(input_frame, text="Año fin:").grid(row=0, column=2, padx=5, pady=5)
        año_fin_entry = tk.Entry(input_frame, width=10)
        año_fin_entry.grid(row=0, column=3, padx=5, pady=5)
        año_fin_entry.insert(0, "2023")
        
        # Área de texto para mostrar resultados
        resultados_text = tk.Text(main_frame, height=15, width=70)
        resultados_text.pack(pady=10, fill='both', expand=True)
        
        def generar_estadisticas():
            """Función interna para generar estadísticas"""
            try:
                año_inicio = int(año_inicio_entry.get())
                año_fin = int(año_fin_entry.get())
                
                # Obtener estadísticas del sistema
                stats = self.sistema.generar_estadisticas_por_año(año_inicio, año_fin)
                
                # Mostrar resultados
                resultados_text.delete(1.0, tk.END)
                resultados_text.insert(tk.END, f"Estadísticas para el rango {año_inicio}-{año_fin}:\n\n")
                resultados_text.insert(tk.END, f"Total de libros: {stats['total_libros']}\n")
                resultados_text.insert(tk.END, f"Total de préstamos: {stats['total_prestamos']}\n")
                
            except ValueError:
                messagebox.showerror("Error", "Por favor ingrese años válidos")
        
        # Botón para generar estadísticas
        tk.Button(main_frame, text="Generar Estadísticas", command=generar_estadisticas,
                 bg='#3498db', fg='white').pack(pady=10)
    
    def mostrar_busquedas_avanzadas(self):
        """Cambia a la pestaña de búsquedas avanzadas"""
        self.notebook.select(self.busquedas_frame)

def main():
    """Función principal que inicia la aplicación"""
    # Crear ventana principal
    root = tk.Tk()
    # Crear instancia de la aplicación
    app = BibliotecaApp(root)
    
    # Centrar la ventana en la pantalla
    root.update_idletasks()
    width = root.winfo_width()
    height = root.winfo_height()
    x = (root.winfo_screenwidth() // 2) - (width // 2)
    y = (root.winfo_screenheight() // 2) - (height // 2)
    root.geometry('{}x{}+{}+{}'.format(width, height, x, y))
    
    # Iniciar el loop principal de la aplicación
    root.mainloop()

# Punto de entrada del programa
if __name__ == "__main__":
    main()