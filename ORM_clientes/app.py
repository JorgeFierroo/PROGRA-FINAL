import customtkinter as ctk
from tkinter import messagebox, ttk
from database import get_session
from crud.ingrediente_crud import IngredienteCRUD
from crud.menu_crud import MenuCRUD
from crud.cliente_crud import ClienteCRUD
from crud.pedido_crud import PedidoCRUD
from database import get_session, engine, Base
# Configuración de la ventana principal
ctk.set_appearance_mode("System")  # Opciones: "System", "Dark", "Light"
ctk.set_default_color_theme("blue")  # Opciones: "blue", "green", "dark-blue"
# Crear las tablas en la base de datos
# Crear las tablas en la base de datos
Base.metadata.create_all(bind=engine)
class App(ctk.CTk):
    def __init__(self):
        super().__init__()

        self.title("Gestión de Clientes, Pedidos y menús")
        self.geometry("1450x600")

        # Crear el Tabview (pestañas)
        self.tabview = ctk.CTkTabview(self)
        self.tabview.pack(pady=20, padx=20, fill="both", expand=True)

        # Pestaña de Ingredientes
        self.tab_ingredientes = self.tabview.add("Ingredientes")
        self.crear_formulario_ingrediente(self.tab_ingredientes)

        # Pestaña de Clientes
        self.tab_menu = self.tabview.add("Menus")
        self.crear_formulario_menu(self.tab_menu) 

        # Pestaña de Clientes
        #self.tab_clientes = self.tabview.add("Clientes")
        #self.crear_formulario_cliente(self.tab_clientes)

        # Pestaña de Clientes
        #self.tab_clientes = self.tabview.add("Panel de compra")
        #self.crear_formulario_cliente(self.tab_clientes)            #cambiar

        # Pestaña de Pedidos
        #self.tab_pedidos = self.tabview.add("Pedidos")
        #self.crear_formulario_pedido(self.tab_pedidos)

        # Pestaña de Clientes
        #self.tab_graficos = self.tabview.add("Graficos")
        #self.crear_formulario_grafico(self.tab_graficos)

        # Revisar el cambio de pestaña periódicamente
        self.current_tab = self.tabview.get()  # Almacena la pestaña actual
        self.after(500, self.check_tab_change)  # Llama a check_tab_change cada 500 ms

    def check_tab_change(self):
        """Revisa si la pestaña activa cambió a 'Pedidos'."""
        new_tab = self.tabview.get()
        if new_tab != self.current_tab:
            self.current_tab = new_tab
            if new_tab == "Pedidos":
                self.actualizar_emails_combobox()
        self.after(500, self.check_tab_change)  # Vuelve a revisar cada 500 ms


##### Formularios #####

    def crear_formulario_ingrediente(self, parent):
        """Crea el formulario en el Frame superior y el Treeview en el Frame inferior para la gestión de clientes."""
        # Frame superior para el formulario y botones
        frame_superior = ctk.CTkFrame(parent)
        frame_superior.pack(pady=10, padx=10, fill="x")

        # Fila 1 - Elementos de la primera fila, no alineados con la segunda fila
        ctk.CTkLabel(frame_superior, text="Nombre").grid(row=0, column=0, pady=10, padx=10)
        self.entry_nombre = ctk.CTkEntry(frame_superior)
        self.entry_nombre.grid(row=0, column=1, pady=10, padx=10)

        ctk.CTkLabel(frame_superior, text="Tipo").grid(row=0, column=2, pady=10, padx=10)
        self.entry_tipo = ctk.CTkEntry(frame_superior)
        self.entry_tipo.grid(row=0, column=3, pady=10, padx=10)

        ctk.CTkLabel(frame_superior, text="Cantidad").grid(row=0, column=4, pady=10, padx=10)
        self.entry_cantidad = ctk.CTkEntry(frame_superior)
        self.entry_cantidad.grid(row=0, column=5, pady=10, padx=10)

        ctk.CTkLabel(frame_superior, text="Unidad").grid(row=0, column=6, pady=10, padx=10)
        self.entry_unidad = ctk.CTkEntry(frame_superior)
        self.entry_unidad.grid(row=0, column=7, pady=10, padx=10)

        # Fila 2 - Botones alineados horizontalmente en la segunda fila
        self.btn_crear_ingrediente = ctk.CTkButton(frame_superior, text="Añadir Ingrediente", command=self.crear_ingrediente)
        self.btn_crear_ingrediente.grid(row=0, column=8, pady=10, padx=10)

        self.btn_actualizar_ingrediente = ctk.CTkButton(frame_superior, text="Actualizar Ingrediente", command=self.actualizar_ingrediente)
        self.btn_actualizar_ingrediente.grid(row=0, column=9, pady=10, padx=10)

        self.btn_eliminar_ingrediente = ctk.CTkButton(frame_superior, text="Eliminar Ingrediente", command=self.eliminar_ingrediente)
        self.btn_eliminar_ingrediente.grid(row=0, column=10, pady=10, padx=10)

        # Frame inferior para el Treeview
        frame_inferior = ctk.CTkFrame(parent)
        frame_inferior.pack(pady=10, padx=10, fill="both", expand=True)

        # Treeview para mostrar los ingredientes
        self.treeview_ingredientes = ttk.Treeview(frame_inferior, columns=("Nombre", "Tipo", "Cantidad","Unidad de medida"), show="headings")
        self.treeview_ingredientes.heading("Nombre", text="Nombre")
        self.treeview_ingredientes.heading("Tipo", text="Tipo")
        self.treeview_ingredientes.heading("Cantidad", text="Cantidad")
        self.treeview_ingredientes.heading("Unidad de medida", text="Unidad de medida")
        self.treeview_ingredientes.pack(pady=10, padx=10, fill="both", expand=True)

        self.cargar_ingredientes()

    def crear_formulario_menu(self, parent):
        """Crea el formulario para crear un menú y seleccionar ingredientes."""
        frame_superior = ctk.CTkFrame(parent)
        frame_superior.pack(pady=10, padx=10, fill="x")

        # Fila para el nombre y descripción del menú
        ctk.CTkLabel(frame_superior, text="Nombre del Menú").grid(row=0, column=0, pady=10, padx=10)
        self.entry_menu_nombre = ctk.CTkEntry(frame_superior)
        self.entry_menu_nombre.grid(row=0, column=1, pady=10, padx=10)

        ctk.CTkLabel(frame_superior, text="Descripción del Menú").grid(row=0, column=2, pady=10, padx=10)
        self.entry_menu_descripcion = ctk.CTkEntry(frame_superior)
        self.entry_menu_descripcion.grid(row=0, column=3, pady=10, padx=10)

        # Fila para seleccionar ingredientes
        ctk.CTkLabel(frame_superior, text="Seleccionar Ingredientes").grid(row=1, column=0, pady=10, padx=10)
        self.combobox_ingredientes = ttk.Combobox(frame_superior, state="readonly")
        self.combobox_ingredientes.grid(row=1, column=1, pady=10, padx=10)

        ctk.CTkLabel(frame_superior, text="Cantidad").grid(row=1, column=2, pady=10, padx=10)
        self.entry_cantidad2 = ctk.CTkEntry(frame_superior)
        self.entry_cantidad2.grid(row=1, column=3, pady=10, padx=10)

        # Botón para agregar ingredientes seleccionados al menú
        self.btn_agregar_ingrediente = ctk.CTkButton(frame_superior, text="Agregar Ingrediente", command=self.agregar_ingrediente)
        self.btn_agregar_ingrediente.grid(row=1, column=4, pady=10, padx=10)

        self.btn_eliminar_ingrediente = ctk.CTkButton(frame_superior, text="Eliminar Ingrediente", command=self.quitar_ingrediente)
        self.btn_eliminar_ingrediente.grid(row=1, column=5, pady=10, padx=10)

        # Botón para crear el menú
        self.btn_crear_menu = ctk.CTkButton(frame_superior, text="Crear Menú", command=self.crear_menu)
        self.btn_crear_menu.grid(row=0, column=4, columnspan=3, pady=10, padx=10)

        # Treeview para mostrar ingredientes añadidos al menú
        self.treeview_ingredientes2 = ttk.Treeview(frame_superior, columns=("Nombre", "Cantidad"), show="headings")
        self.treeview_ingredientes2.heading("Nombre", text="Nombre")
        self.treeview_ingredientes2.heading("Cantidad", text="Cantidad")
        self.treeview_ingredientes2.grid(row=3, column=0, columnspan=3, pady=10, padx=10, sticky="nsew")
        self.actualizar_combobox_ingredientes()



    def crear_formulario_cliente(self, parent):
        """Crea el formulario en el Frame superior y el Treeview en el Frame inferior para la gestión de clientes."""
        # Frame superior para el formulario y botones
        frame_superior = ctk.CTkFrame(parent)
        frame_superior.pack(pady=10, padx=10, fill="x")

        ctk.CTkLabel(frame_superior, text="Nombre").grid(row=0, column=0, pady=10, padx=10)
        self.entry_nombre = ctk.CTkEntry(frame_superior)
        self.entry_nombre.grid(row=0, column=1, pady=10, padx=10)

        ctk.CTkLabel(frame_superior, text="Email").grid(row=0, column=2, pady=10, padx=10)
        self.entry_email = ctk.CTkEntry(frame_superior)
        self.entry_email.grid(row=0, column=3, pady=10, padx=10)

        # Botones alineados horizontalmente en el frame superior
        self.btn_crear_cliente = ctk.CTkButton(frame_superior, text="Crear Cliente", command=self.crear_cliente)
        self.btn_crear_cliente.grid(row=1, column=0, pady=10, padx=10)

        self.btn_actualizar_cliente = ctk.CTkButton(frame_superior, text="Actualizar Cliente", command=self.actualizar_cliente)
        self.btn_actualizar_cliente.grid(row=1, column=1, pady=10, padx=10)

        self.btn_eliminar_cliente = ctk.CTkButton(frame_superior, text="Eliminar Cliente", command=self.eliminar_cliente)
        self.btn_eliminar_cliente.grid(row=1, column=2, pady=10, padx=10)

        # Frame inferior para el Treeview
        frame_inferior = ctk.CTkFrame(parent)
        frame_inferior.pack(pady=10, padx=10, fill="both", expand=True)

        # Treeview para mostrar los clientes
        self.treeview_clientes = ttk.Treeview(frame_inferior, columns=("Email", "Nombre"), show="headings")
        self.treeview_clientes.heading("Email", text="Email")
        self.treeview_clientes.heading("Nombre", text="Nombre")
        self.treeview_clientes.pack(pady=10, padx=10, fill="both", expand=True)

        #self.cargar_clientes()

    def crear_formulario_panel_de_compra(self, parent):
        """Crea el formulario en el Frame superior y el Treeview en el Frame inferior para la gestión de clientes."""
        # Frame superior para el formulario y botones
        frame_superior = ctk.CTkFrame(parent)
        frame_superior.pack(pady=10, padx=10, fill="x")

        ctk.CTkLabel(frame_superior, text="Menú").grid(row=0, column=0, pady=10, padx=10)
        self.entry_nombre = ctk.CTkEntry(frame_superior)
        self.entry_nombre.grid(row=0, column=1, pady=10, padx=10)

        # Combobox para seleccionar el email del cliente
        self.combobox_cliente_email = ttk.Combobox(frame_superior, state="readonly")
        self.combobox_cliente_email.grid(row=0, column=1, pady=10, padx=10)
        self.actualizar_emails_combobox()  # Llenar el combobox con emails de los clientes

        # Botones alineados horizontalmente en el frame superior
        self.btn_crear_cliente = ctk.CTkButton(frame_superior, text="Agregar a la compra", command=self.crear_cliente)
        self.btn_crear_cliente.grid(row=1, column=0, pady=10, padx=10)

        # Frame inferior para el Treeview
        frame_inferior = ctk.CTkFrame(parent)
        frame_inferior.pack(pady=10, padx=10, fill="both", expand=True)

        # Treeview para mostrar los clientes
        self.treeview_clientes = ttk.Treeview(frame_inferior, columns=("Nombre", "Tipo"), show="headings")
        self.treeview_clientes.heading("Nombre", text="Nombre")
        self.treeview_clientes.heading("Tipo", text="Tipo")
        self.treeview_clientes.pack(pady=10, padx=10, fill="both", expand=True)

    def crear_formulario_pedido(self, parent):
        """Crea el formulario en el Frame superior y el Treeview en el Frame inferior para la gestión de pedidos."""
        # Frame superior para el formulario y botones
        frame_superior = ctk.CTkFrame(parent)
        frame_superior.pack(pady=10, padx=10, fill="x")

        ctk.CTkLabel(frame_superior, text="Cliente Email").grid(row=0, column=0, pady=10, padx=10)
        
        # Combobox para seleccionar el email del cliente
        self.combobox_cliente_email = ttk.Combobox(frame_superior, state="readonly")
        self.combobox_cliente_email.grid(row=0, column=1, pady=10, padx=10)
        self.actualizar_emails_combobox()  # Llenar el combobox con emails de los clientes

        ctk.CTkLabel(frame_superior, text="Descripción").grid(row=0, column=2, pady=10, padx=10)
        self.entry_descripcion = ctk.CTkEntry(frame_superior)
        self.entry_descripcion.grid(row=0, column=3, pady=10, padx=10)

        # Botones alineados horizontalmente en el frame superior
        self.btn_crear_pedido = ctk.CTkButton(frame_superior, text="Crear Pedido", command=self.crear_pedido)
        self.btn_crear_pedido.grid(row=1, column=0, pady=10, padx=10)

        self.btn_actualizar_pedido = ctk.CTkButton(frame_superior, text="Actualizar Pedido", command=self.actualizar_pedido)
        self.btn_actualizar_pedido.grid(row=1, column=1, pady=10, padx=10)

        self.btn_eliminar_pedido = ctk.CTkButton(frame_superior, text="Eliminar Pedido", command=self.eliminar_pedido)
        self.btn_eliminar_pedido.grid(row=1, column=2, pady=10, padx=10)

        # Frame inferior para el Treeview
        frame_inferior = ctk.CTkFrame(parent)
        frame_inferior.pack(pady=10, padx=10, fill="both", expand=True)

        # Treeview para mostrar los pedidos
        self.treeview_pedidos = ttk.Treeview(frame_inferior, columns=("ID", "Cliente Email", "Descripción"), show="headings")
        self.treeview_pedidos.heading("ID", text="ID")
        self.treeview_pedidos.heading("Cliente Email", text="Cliente Email")
        self.treeview_pedidos.heading("Descripción", text="Descripción")
        self.treeview_pedidos.pack(pady=10, padx=10, fill="both", expand=True)

        self.cargar_pedidos()

    def crear_formulario_grafico(self, parent):
        """Crea el formulario en el Frame superior y el Treeview en el Frame inferior para la gestión de clientes."""
        # Frame superior para el formulario y botones
        frame_superior = ctk.CTkFrame(parent)
        frame_superior.pack(pady=10, padx=10, fill="x")

        ctk.CTkLabel(frame_superior, text="Nombre").grid(row=0, column=0, pady=10, padx=10)
        self.entry_nombre = ctk.CTkEntry(frame_superior)
        self.entry_nombre.grid(row=0, column=1, pady=10, padx=10)

        ctk.CTkLabel(frame_superior, text="Tipo").grid(row=0, column=2, pady=10, padx=10)
        self.entry_tipo = ctk.CTkEntry(frame_superior)
        self.entry_tipo.grid(row=0, column=3, pady=10, padx=10)

        # Botones alineados horizontalmente en el frame superior
        self.btn_crear_cliente = ctk.CTkButton(frame_superior, text="Crear Ingrediete", command=self.crear_cliente)
        self.btn_crear_cliente.grid(row=1, column=0, pady=10, padx=10)

        # Frame inferior para el Treeview
        frame_inferior = ctk.CTkFrame(parent)
        frame_inferior.pack(pady=10, padx=10, fill="both", expand=True)

        # Treeview para mostrar los clientes
        self.treeview_clientes = ttk.Treeview(frame_inferior, columns=("Nombre", "Tipo"), show="headings")
        self.treeview_clientes.heading("Nombre", text="Nombre")
        self.treeview_clientes.heading("Tipo", text="Tipo")
        self.treeview_clientes.pack(pady=10, padx=10, fill="both", expand=True)

    # Método para actualizar los correos electrónicos en el Combobox
    def actualizar_emails_combobox(self):
        """Llena el Combobox con los emails de los clientes."""
        db = next(get_session())
        emails = [cliente.email for cliente in ClienteCRUD.leer_cliente(db)]
        self.combobox_cliente_email['values'] = emails
        db.close()
    
    # Métodos CRUD para Clientes
    def cargar_clientes(self):
        db = next(get_session())
        self.treeview_clientes.delete(*self.treeview_clientes.get_children())
        clientes = ClienteCRUD.leer_cliente(db)
        for cliente in clientes:
            self.treeview_clientes.insert("", "end", values=(cliente.email, cliente.nombre, cliente.edad))
        db.close()

    def crear_cliente(self):
        nombre = self.entry_nombre.get()
        email = self.entry_email.get()
        edad = self.entry_edad.get()
        if nombre and email:
            db = next(get_session())
            cliente = ClienteCRUD.crear_cliente(db, nombre, email,edad)
            if cliente:
                messagebox.showinfo("Éxito", "Cliente creado correctamente.")
                self.cargar_clientes()
                self.actualizar_emails_combobox()  # Actualizar el Combobox con el nuevo email
            else:
                messagebox.showwarning("Error", "El cliente ya existe.")
            db.close()
        else:
            messagebox.showwarning("Campos Vacíos", "Por favor, ingrese todos los campos.")

    def actualizar_cliente(self):
        selected_item = self.treeview_clientes.selection()
        if not selected_item:
            messagebox.showwarning("Selección", "Por favor, seleccione un cliente.")
            return
        nombre = self.entry_nombre.get()
        email = self.entry_email.get()
        edad = self.entry_edad.get()
        if not nombre.strip():
            messagebox.showwarning("Campo Vacío", "Por favor, ingrese un nombre.")
            return
        if not email.strip():
            messagebox.showwarning("Campo Vacío", "Por favor, ingrese un email.")
            return
        email_viejo = self.treeview_clientes.item(selected_item)["values"][0]
        nombre = self.entry_nombre.get()
        edad=self.entry_edad.get()
        if nombre:
            db = next(get_session())
            cliente_actualizado = ClienteCRUD.actualizar_cliente(db, email_viejo, nombre,email,edad)
            if cliente_actualizado:
                messagebox.showinfo("Éxito", "Cliente actualizado correctamente.")
                self.cargar_clientes()
            else:
                messagebox.showwarning("Error", "No se pudo actualizar el cliente.")
            db.close()
        else:
            messagebox.showwarning("Campos Vacíos", "Por favor, ingrese el nombre.")

    def eliminar_cliente(self):
        selected_item = self.treeview_clientes.selection()
        if not selected_item:
            messagebox.showwarning("Selección", "Por favor, seleccione un cliente.")
            return
        email = self.treeview_clientes.item(selected_item)["values"][0]
        db = next(get_session())
        ClienteCRUD.borrar_cliente(db, email)
        messagebox.showinfo("Éxito", "Cliente eliminado correctamente.")
        self.cargar_clientes()
        self.actualizar_emails_combobox()  # Actualizar el Combobox después de eliminar
        db.close()

    # Métodos CRUD para Pedidos
    def cargar_pedidos(self):
        db = next(get_session())
        self.treeview_pedidos.delete(*self.treeview_pedidos.get_children())
        pedidos = PedidoCRUD.leer_pedidos(db)
        for pedido in pedidos:
            self.treeview_pedidos.insert("", "end", values=(pedido.id, pedido.cliente_email, pedido.descripcion))
        db.close()

    def crear_pedido(self):
        cliente_email = self.combobox_cliente_email.get()
        descripcion = self.entry_descripcion.get()
        if cliente_email and descripcion:
            db = next(get_session())
            pedido = PedidoCRUD.crear_pedido(db, cliente_email, descripcion)
            if pedido:
                messagebox.showinfo("Éxito", "Pedido creado correctamente.")
                self.cargar_pedidos()
            else:
                messagebox.showwarning("Error", "No se pudo crear el pedido.")
            db.close()
        else:
            messagebox.showwarning("Campos Vacíos", "Por favor, ingrese todos los campos.")

    def actualizar_pedido(self):
        selected_item = self.treeview_pedidos.selection()
        if not selected_item:
            messagebox.showwarning("Selección", "Por favor, seleccione un pedido.")
            return
        pedido_id = self.treeview_pedidos.item(selected_item)["values"][0]
        descripcion = self.entry_descripcion.get()
        if descripcion:
            db = next(get_session())
            pedido_actualizado = PedidoCRUD.actualizar_pedido(db, pedido_id, descripcion)
            if pedido_actualizado:
                messagebox.showinfo("Éxito", "Pedido actualizado correctamente.")
                self.cargar_pedidos()
            else:
                messagebox.showwarning("Error", "No se pudo actualizar el pedido.")
            db.close()
        else:
            messagebox.showwarning("Campos Vacíos", "Por favor, ingrese la descripción.")

    def eliminar_pedido(self):
        selected_item = self.treeview_pedidos.selection()
        if not selected_item:
            messagebox.showwarning("Selección", "Por favor, seleccione un pedido.")
            return
        pedido_id = self.treeview_pedidos.item(selected_item)["values"][0]
        db = next(get_session())
        PedidoCRUD.borrar_pedido(db, pedido_id)
        messagebox.showinfo("Éxito", "Pedido eliminado correctamente.")
        self.cargar_pedidos()
        db.close()
        
    def crear_ingrediente(self):
        nombre = self.entry_nombre.get()
        tipo = self.entry_tipo.get()
        cantidad = self.entry_cantidad.get()
        unidad = self.entry_unidad.get()
        if nombre and tipo and cantidad and unidad:
            db = next(get_session())
            ingrediente = IngredienteCRUD.crear_ingrediente(db, nombre, tipo, cantidad, unidad)
            if ingrediente:
                messagebox.showinfo("Exito","Ingrediente ingresado correctamente")
                self.cargar_ingredientes()
            else:
                messagebox.showwarning("Error", "El ingrediente ya existe.")
            db.close()
        else:
            messagebox.showwarning("Campos Vacíos", "Por favor, ingrese todos los campos.")


    def actualizar_ingrediente(self):
        selected_item = self.treeview_ingredientes.selection()
        if not selected_item:
            messagebox.showwarning("Selección", "Por favor, seleccione un ingrediente.")
            return
    
        # Obteniendo valores de los campos de entrada
        nombre = self.entry_nombre.get().strip()
        tipo = self.entry_tipo.get().strip()
        cantidad = self.entry_cantidad.get().strip()
        unidad = self.entry_unidad.get().strip()
    
        # Validación de campos
        if not nombre:
            messagebox.showwarning("Campo Vacío", "Por favor, ingrese un nombre.")
            return
        if not tipo:
            messagebox.showwarning("Campo Vacío", "Por favor, ingrese un tipo.")
            return
        if not cantidad:
            messagebox.showwarning("Campo Vacío", "Por favor, ingrese una cantidad.")
            return
        if not unidad:
            messagebox.showwarning("Campo Vacío", "Por favor, ingrese una unidad.")
            return
    
        # Nombre viejo para actualizar
        nombre_viejo = self.treeview_ingredientes.item(selected_item)["values"][0]
    
        # Conexión a la base de datos y actualización
        db = next(get_session())
        ingrediente_actualizado = IngredienteCRUD.actualizar_ingrediente(db, nombre_viejo,nombre, tipo, cantidad, unidad)
        db.close()
    
        # Verificación de resultado
        if ingrediente_actualizado:
            messagebox.showinfo("Éxito", "Cliente actualizado correctamente.")
            self.cargar_ingredientes()
        else:
            messagebox.showwarning("Error", "No se pudo actualizar el cliente.")


    def eliminar_ingrediente(self):
        selected_item = self.treeview_ingredientes.selection()
        if not selected_item:
            messagebox.showwarning("Selección", "Por favor, seleccione un ingrediente.")
            return
        nombre = self.treeview_ingredientes.item(selected_item)["values"][0]
        db = next(get_session())
        IngredienteCRUD.borrar_ingrediente(db, nombre)
        messagebox.showinfo("Éxito", "Ingrediente eliminado correctamente.")
        self.cargar_ingredientes()

        db.close()

    def cargar_ingredientes(self):
        db = next(get_session())
        self.treeview_ingredientes.delete(*self.treeview_ingredientes.get_children())
        ingredientes = IngredienteCRUD.leer_ingredientes(db)
        for ingrediente in ingredientes:
            self.treeview_ingredientes.insert("", "end", values=(ingrediente.nombre, ingrediente.tipo,ingrediente.cantidad,ingrediente.unidad))
        db.close()

    def actualizar_combobox_ingredientes(self):
        """Actualiza el Combobox con los ingredientes disponibles en la base de datos."""
        db = next(get_session())
        ingredientes = IngredienteCRUD.leer_ingredientes(db)
        nuevos_valores = [ingrediente.nombre for ingrediente in ingredientes]
        db.close()

        # Verificar si los valores han cambiado para evitar actualizaciones innecesarias
        if self.combobox_ingredientes["values"] != tuple(nuevos_valores):
            self.combobox_ingredientes["values"] = nuevos_valores

        # Llamar a este método nuevamente después de 1000 ms (1 segundo)
        self.after(1000, self.actualizar_combobox_ingredientes)

    def cargar_menus(self):
        db = next(get_session())
        self.treeview_menus.delete(*self.treeview_menus.get_children())
        menus = MenuCRUD.leer_menus(db)
        for menu in menus:
            self.treeview_menus.insert("", "end", values=(menu.nombre, menu.descripcion))
        db.close()

    def crear_menu(self):
        db = next(get_session())
        # Obtener el nombre y la descripción del menú
        nombre_menu = self.entry_menu_nombre.get()
        descripcion_menu = self.entry_menu_descripcion.get()

        if not nombre_menu or not descripcion_menu:
            # Mostrar un mensaje de error si falta el nombre o la descripción
            messagebox.showerror("Error", "El nombre y la descripción son obligatorios.")
            return

        # Crear un objeto Menu
        nuevo_menu = Menu(nombre=nombre_menu, descripcion=descripcion_menu)

        # Obtener los ingredientes del Treeview
        ingredientes_seleccionados = []
        for item in self.treeview_ingredientes2.get_children():
            nombre_ingrediente = self.treeview_ingredientes2.item(item, "values")[0]
            cantidad_ingrediente = self.treeview_ingredientes2.item(item, "values")[1]
        
            # Buscar el ingrediente en la base de datos
        ingrediente = db.query(Ingrediente).filter_by(nombre=nombre_ingrediente).first()

        if ingrediente:
            # Asignar la cantidad del ingrediente
            ingrediente_menu = {"ingrediente": ingrediente, "cantidad": cantidad_ingrediente}
            ingredientes_seleccionados.append(ingrediente_menu)

        # Asociar los ingredientes al nuevo menú
        for ingrediente in ingredientes_seleccionados:
            ingrediente_obj = ingrediente["ingrediente"]
            # Aquí debes agregar la lógica para asociar la cantidad con el ingrediente (si es necesario).
            # Podrías usar una tabla intermedia para almacenar la relación entre menú e ingrediente junto con la cantidad
            nuevo_menu.ingredientes.append(ingrediente_obj)

                # Guardar el menú en la base de datos
        db.add(nuevo_menu)
        db.commit()

        # Confirmar la creación
        messagebox.showinfo("Éxito", f"Menú '{nombre_menu}' creado con éxito.")
    
        # Limpiar los campos
        self.entry_menu_nombre.delete(0, 'end')
        self.entry_menu_descripcion.delete(0, 'end')
        self.treeview_ingredientes2.delete(*self.treeview_ingredientes2.get_children())


    def eliminar_menu(self):
        selected_item = self.treeview_menus.selection()
        if not selected_item:
            messagebox.showwarning("Selección", "Por favor, seleccione un menú.")
            return

        nombre = self.treeview_menus.item(selected_item)["values"][0]
        db = next(get_session())
        MenuCRUD.borrar_menu(db, nombre)
        db.close()

        messagebox.showinfo("Éxito", "Menú eliminado correctamente.")
        self.cargar_menus()

    def agregar_ingrediente(self):
        """Agrega el ingrediente seleccionado al menú."""
        ingrediente_seleccionado = self.combobox_ingredientes.get()
        cantidad_seleccionada = self.entry_cantidad2.get()
        if ingrediente_seleccionado:
            # Agregar el ingrediente al Treeview
            self.treeview_ingredientes2.insert("", "end", values=(ingrediente_seleccionado, cantidad_seleccionada))

    def quitar_ingrediente(self):
        # Obtener el ítem seleccionado en el Treeview
        seleccion = self.treeview_ingredientes2.selection()
        if seleccion:
            # Eliminar el ítem seleccionado
            self.treeview_ingredientes2.delete(seleccion)
        else:
            # Mensaje de advertencia si no se selecciona ningún ingrediente
            print("Por favor, seleccione un ingrediente para eliminar.")


    def crear_menu(self):
        """Crear un menú con los ingredientes seleccionados."""
        nombre_menu = self.entry_menu_nombre.get()
        descripcion_menu = self.entry_menu_descripcion.get()

        if not nombre_menu or not descripcion_menu:
            messagebox.showwarning("Campos Vacíos", "Por favor, ingrese todos los campos del menú.")
            return

        # Crear el menú en la base de datos
        db = next(get_session())
        menu = MenuCRUD.crear_menu(db, nombre_menu, descripcion_menu)
        
        # Aquí agregarías los ingredientes seleccionados al menú creado
        for item in self.treeview_ingredientes.get_children():
            nombre_ingrediente = self.treeview_ingredientes.item(item)["values"][0]
            ingrediente = db.query(ingrediente).filter(ingrediente.nombre == nombre_ingrediente).first()
            menu.ingredientes.append(ingrediente)
        
        db.add(menu)
        db.commit()
        db.close()

        messagebox.showinfo("Éxito", "Menú creado correctamente.")


if __name__ == "__main__":
    app = App()
    app.mainloop()
