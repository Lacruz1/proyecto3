import tkinter as tk
from tkinter import messagebox
import json
import os
from datetime import datetime
from principal.modelos import Doctor, Paciente
from principal.autenticacion import ErrorDeLogin

# Excepciones personalizadas para el proyecto
class ErrorDeValidacion(Exception):
    #se muestra si dejan algun campo vacio
    pass

class AplicacionMedico:
    #Configura la ventana principal,
    #inicializa las estructuras de datos
    #y decide qué pantalla mostrar al inicio.
    def __init__(self, root):
        self.root = root
        self.root.title("Sistema Médico Universitario - Eduard Lacruz")
        self.root.geometry("550x650")
        
        self.archivo_bd = "datos.json"
        self.lista_pacientes = []
        self.doctor_sistema = None
        
        self.contenedor = tk.Frame(self.root)
        self.contenedor.pack(fill="both", expand=True, padx=20, pady=20)
        
        self.cargar_datos()

        if self.doctor_sistema:
            self.pantalla_login()
        else:
            self.pantalla_registro_doctor()

    #transforma los datos y descompone los objetos
    #para que el json los lea y guarde correctamente
    def guardar_datos(self):
        try:
            datos = {
                 "doctor": {
                    "nombre": self.doctor_sistema.nombre,
                    "edad": self.doctor_sistema.edad,
                    "usuario": self.doctor_sistema.usuario,
                    "clave": self.doctor_sistema.clave
                } if self.doctor_sistema else None,
                "pacientes": [
                    {
                        "nombre": p.nombre, "edad": p.edad,
                        "padecimientos": p.padecimientos, "peso": p.peso,
                        "historial": p.historial
                    } for p in self.lista_pacientes
                ]
            }
            with open(self.archivo_bd, "w") as f:
                json.dump(datos, f, indent=4)
        except Exception as e:
            messagebox.showerror("Error", f"No se pudo guardar: {e}")

    #verifica que exista el archivo con los datos y vuelve a organizar los objetos
    def cargar_datos(self):
        if os.path.exists(self.archivo_bd):
            try:
                with open(self.archivo_bd, "r") as f:
                    datos = json.load(f)
                    if datos.get("doctor"):
                        d = datos["doctor"]
                        self.doctor_sistema = Doctor(d["nombre"], d["edad"], d["usuario"], d["clave"])
                    
                    for p in datos.get("pacientes", []):
                        nuevo = Paciente(p["nombre"], p["edad"], p["padecimientos"], p["peso"], p.get("historial", []))
                        self.lista_pacientes.append(nuevo)
            except:
                pass # Si el archivo está vacío o mal formado, inicia de cero

    #limpia la pantalla y vuelve a cargar
    #los datos nuevos para mostrar lo que se selecciona
    def limpiar_pantalla(self):
        for w in self.contenedor.winfo_children(): w.destroy()

    #FLUJO DE PANTALLAS

    #muetra el primer formulario,
    #solo es la primera vez para registrar el primer doctor
    def pantalla_registro_doctor(self):
        self.limpiar_pantalla()
        tk.Label(self.contenedor, text="REGISTRO ÚNICO DEL DOCTOR", font=("Arial", 12, "bold")).pack(pady=10)
        
        campos = ["Nombre", "Edad", "Usuario", "Clave"]
        ents = {}
        for c in campos:
            tk.Label(self.contenedor, text=c).pack()
            e = tk.Entry(self.contenedor, show="*" if c == "Clave" else "")
            e.pack()
            ents[c] = e

        def registrar():
            try:
                # VALIDACIÓN: Campos vacíos
                if not all(ents[c].get().strip() for c in campos):
                    raise ErrorDeValidacion("Todos los campos son obligatorios.")
                # VALIDACIÓN: Edad numérica
                if not ents["Edad"].get().isdigit():
                    raise ErrorDeValidacion("La edad debe ser un número.")

                self.doctor_sistema = Doctor(ents["Nombre"].get(), ents["Edad"].get(), 
                                           ents["Usuario"].get(), ents["Clave"].get())
                self.guardar_datos()
                messagebox.showinfo("Éxito", "Doctor registrado.")
                self.pantalla_login()
            except ErrorDeValidacion as e:
                messagebox.showwarning("Atención", str(e))

        tk.Button(self.contenedor, text="Finalizar Registro", command=registrar, bg="#2ecc71", fg="white").pack(pady=20)

    #cuando yua hay un doctor guardado
    #pude los datos de ese doctor para poder entrar
    def pantalla_login(self):
        self.limpiar_pantalla()
        tk.Label(self.contenedor, text=f"Bienvenido Dr. {self.doctor_sistema.nombre}", font=("Arial", 11)).pack(pady=10)
        
        tk.Label(self.contenedor, text="Usuario:").pack()
        u = tk.Entry(self.contenedor); u.pack()
        tk.Label(self.contenedor, text="Clave:").pack()
        c = tk.Entry(self.contenedor, show="*"); c.pack()

        def entrar():
            try:
                if self.doctor_sistema.Validar_acceso(u.get(), c.get()):
                    self.menu_principal()
            except ErrorDeLogin as e:
                messagebox.showerror("Acceso Denegado", str(e))

        tk.Button(self.contenedor, text="Iniciar Sesión", command=entrar, width=15).pack(pady=15)

    def menu_principal(self):
        #muestra el menu
        self.limpiar_pantalla()
        tk.Label(self.contenedor, text="PANEL DE GESTIÓN", font=("Arial", 14, "bold")).pack(pady=20)
        
        btns = [
            ("Registrar Nuevo Paciente", self.form_paciente),
            ("Listado y Consultas", self.ver_pacientes),
            ("Cerrar Sesión", self.pantalla_login),
            ("Salir del Programa", self.root.quit)
        ]
        for t, c in btns:
            tk.Button(self.contenedor, text=t, width=30, pady=5, command=c).pack(pady=5)

    #muestra el formulario para guardar datos del paciente
    def form_paciente(self):
        self.limpiar_pantalla()
        tk.Label(self.contenedor, text="REGISTRO DE PACIENTE", font=("Arial", 12)).pack(pady=10)
        
        campos = ["Nombre", "Edad", "Peso", "Padecimientos"]
        ents = {}
        for c in campos:
            tk.Label(self.contenedor, text=c).pack()
            e = tk.Entry(self.contenedor); e.pack()
            ents[c] = e

        def guardar():
            try:
                # VALIDACIONES
                if not ents["Nombre"].get() or not ents["Edad"].get():
                    raise ErrorDeValidacion("Nombre y Edad son obligatorios.")
                if not ents["Edad"].get().isdigit():
                    raise ErrorDeValidacion("La edad debe ser numérica.")

                p = Paciente(ents["Nombre"].get(), ents["Edad"].get(), 
                             ents["Padecimientos"].get(), ents["Peso"].get())
                self.lista_pacientes.append(p)
                self.guardar_datos()
                messagebox.showinfo("Éxito", "Paciente guardado.")
                self.menu_principal()
            except ErrorDeValidacion as e:
                messagebox.showwarning("Error", str(e))

        tk.Button(self.contenedor, text="Guardar Paciente", command=guardar, bg="#3498db", fg="white").pack(pady=15)
        tk.Button(self.contenedor, text="Volver", command=self.menu_principal).pack()

    #crea una lista visual escroleable
    #para mostrar los pacientes y sus datos generales
    def ver_pacientes(self):
        self.limpiar_pantalla()
        tk.Label(self.contenedor, text="BUSCAR PACIENTE:", font=("Arial", 10)).pack()
        busqueda = tk.Entry(self.contenedor)
        busqueda.pack(pady=5)
        
        lista_frame = tk.Frame(self.contenedor)
        lista_frame.pack(fill="both", expand=True)

        def filtrar():
            for w in lista_frame.winfo_children(): w.destroy()
            texto = busqueda.get().lower()
            for p in self.lista_pacientes:
                if texto in p.nombre.lower():
                    f = tk.Frame(lista_frame, relief="groove", borderwidth=1)
                    f.pack(fill="x", pady=2)
                    tk.Label(f, text=f"{p.nombre} ({p.edad} años)", width=20, anchor="w").pack(side="left")
                    tk.Button(f, text="+ Consulta", command=lambda obj=p: self.pantalla_consulta(obj)).pack(side="right")

        busqueda.bind("<KeyRelease>", lambda e: filtrar())
        filtrar()
        tk.Button(self.contenedor, text="Menu Principal", command=self.menu_principal).pack(pady=10)

    def pantalla_consulta(self, paciente):
        self.limpiar_pantalla()
        tk.Label(self.contenedor, text=f"CONSULTA: {paciente.nombre}", font=("Arial", 12, "bold")).pack(pady=10)
        
        # Mostrar historial previo
        hist_text = ""
        for c in paciente.historial:
            hist_text += f"{c['fecha']}: {c['nota']}\n"
        
        tk.Label(self.contenedor, text="Historial anterior:").pack()
        log = tk.Text(self.contenedor, height=8, width=50)
        log.insert("1.0", hist_text if hist_text else "Sin consultas previas.")
        log.config(state="disabled")
        log.pack(pady=5)

        tk.Label(self.contenedor, text="Nueva nota médica:").pack()
        nueva_nota = tk.Entry(self.contenedor, width=50)
        nueva_nota.pack(pady=5)

        def registrar_nota():
            if nueva_nota.get():
                fecha = datetime.now().strftime("%d/%m/%Y")
                paciente.agregar_consulta(fecha, nueva_nota.get())
                self.guardar_datos()
                messagebox.showinfo("Éxito", "Consulta registrada.")
                self.ver_pacientes()

        tk.Button(self.contenedor, text="Guardar Nota", command=registrar_nota, bg="green", fg="white").pack(pady=10)
        tk.Button(self.contenedor, text="Volver", command=self.ver_pacientes).pack()

if __name__ == "__main__":
    root = tk.Tk()
    app = AplicacionMedico(root)
    root.mainloop()