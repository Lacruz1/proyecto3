import tkinter as tk
from tkinter import messagebox
from datetime import datetime
import logging

# Importes internos
from principal.modelos import Doctor, Paciente
from principal.autenticacion import ErrorDeLogin
from principal.persistencia import GestorDatos

# clase principal
class AplicacionMedico:
    def __init__(self, root):
        self.root = root
        self.root.title("Sistema Médico Universitario")
        self.root.geometry("550x650")
        
        # Datos compartidos
        self.gestor_datos = GestorDatos()
        self.doctor_sistema, self.lista_pacientes = self.gestor_datos.cargar()
        
        # Contenedor principal
        self.contenedor = tk.Frame(self.root)
        self.contenedor.pack(fill="both", expand=True, padx=20, pady=20)
        
        self.iniciar_flujo()

    def iniciar_flujo(self):
        if self.doctor_sistema:
            self.cambiar_vista(VistaLogin)
        else:
            self.cambiar_vista(VistaRegistroDoctor)

    def cambiar_vista(self, clase_vista, **kwargs):
        # actualiza la vista, se elimina el anterios y cambia por el nuevo
        for w in self.contenedor.winfo_children():
            w.destroy()
        
        clase_vista(self.contenedor, self, **kwargs)

    def actualizar_persistencia(self):
        try:
            self.gestor_datos.guardar(self.doctor_sistema, self.lista_pacientes)
        except Exception as e:
            messagebox.showerror("Error", f"No se pudo guardar: {e}")

# vista de registro del doctor
class VistaRegistroDoctor:
    def __init__(self, master, app):
        tk.Label(master, text="REGISTRO ÚNICO DEL DOCTOR", font=("Arial", 12, "bold")).pack(pady=10)
        
        campos = ["Nombre", "Edad", "Usuario", "Clave"]
        self.ents = {}
        for c in campos:
            tk.Label(master, text=c).pack()
            e = tk.Entry(master, show="*" if c == "Clave" else "")
            e.pack()
            self.ents[c] = e

        tk.Button(master, text="Finalizar Registro", bg="#2ecc71", fg="white",
                  command=lambda: self.validar(app)).pack(pady=20)

    def validar(self, app):
        if not all(self.ents[c].get().strip() for c in self.ents):
            return messagebox.showwarning("Atención", "Campos incompletos")
        
        app.doctor_sistema = Doctor(self.ents["Nombre"].get(), self.ents["Edad"].get(), 
                                   self.ents["Usuario"].get(), self.ents["Clave"].get())
        app.actualizar_persistencia()
        app.cambiar_vista(VistaLogin)

# vista del login
class VistaLogin:
    def __init__(self, master, app):
        tk.Label(master, text=f"Bienvenido Dr. {app.doctor_sistema.nombre}", font=("Arial", 11)).pack(pady=10)
        
        tk.Label(master, text="Usuario:").pack()
        u = tk.Entry(master); u.pack()
        tk.Label(master, text="Clave:").pack()
        c = tk.Entry(master, show="*"); c.pack()

        tk.Button(master, text="Entrar", width=15, 
                  command=lambda: self.intentar(app, u.get(), c.get())).pack(pady=15)

    def intentar(self, app, user, pwd):
        try:
            if app.doctor_sistema.Validar_acceso(user, pwd):
                app.cambiar_vista(VistaMenuPrincipal)
        except ErrorDeLogin as e:
            messagebox.showerror("Error", str(e))

# vista menu principal
class VistaMenuPrincipal:
    def __init__(self, master, app):
        tk.Label(master, text="PANEL DE GESTIÓN", font=("Arial", 14, "bold")).pack(pady=20)
        
        opciones = [
            ("Registrar Paciente", lambda: app.cambiar_vista(VistaFormPaciente)),
            ("Listado y Consultas", lambda: app.cambiar_vista(VistaListadoPacientes)),
            ("Cerrar Sesión", lambda: app.cambiar_vista(VistaLogin)),
            ("Salir", app.root.quit)
        ]
        for texto, comando in opciones:
            tk.Button(master, text=texto, width=30, pady=5, command=comando).pack(pady=5)

# vista del formulario del paciente
class VistaFormPaciente:
    def __init__(self, master, app):
        tk.Label(master, text="REGISTRO DE PACIENTE", font=("Arial", 12)).pack(pady=10)
        self.ents = {}
        for c in ["Nombre", "Edad", "Peso", "Padecimientos"]:
            tk.Label(master, text=c).pack()
            e = tk.Entry(master); e.pack(); self.ents[c] = e

        tk.Button(master, text="Guardar", bg="#3498db", fg="white", 
                  command=lambda: self.guardar(app)).pack(pady=15)
        tk.Button(master, text="Volver", command=lambda: app.cambiar_vista(VistaMenuPrincipal)).pack()

    def guardar(self, app):
        p = Paciente(self.ents["Nombre"].get(), self.ents["Edad"].get(), 
                     self.ents["Padecimientos"].get(), self.ents["Peso"].get())
        app.lista_pacientes.append(p)
        app.actualizar_persistencia()
        app.cambiar_vista(VistaMenuPrincipal)

# vista del listado y busqueda por paciente
class VistaListadoPacientes:
    def __init__(self, master, app):
        tk.Label(master, text="BUSCAR PACIENTE:").pack()
        busqueda = tk.Entry(master); busqueda.pack(pady=5)
        self.lista_frame = tk.Frame(master); self.lista_frame.pack(fill="both", expand=True)

        def filtrar(e=None):
            for w in self.lista_frame.winfo_children(): w.destroy()
            for p in app.lista_pacientes:
                if busqueda.get().lower() in p.nombre.lower():
                    f = tk.Frame(self.lista_frame, relief="groove", borderwidth=1)
                    f.pack(fill="x", pady=2)
                    tk.Label(f, text=p.nombre, width=20, anchor="w").pack(side="left")
                    tk.Button(f, text="+ Consulta", command=lambda obj=p: app.cambiar_vista(VistaConsulta, paciente=obj)).pack(side="right")

        busqueda.bind("<KeyRelease>", filtrar)
        filtrar()
        tk.Button(master, text="Menu Principal", command=lambda: app.cambiar_vista(VistaMenuPrincipal)).pack(pady=10)

# vista del detalle de una consulta
class VistaConsulta:
    def __init__(self, master, app, paciente):
        tk.Label(master, text=f"CONSULTA: {paciente.nombre}", font=("Arial", 12, "bold")).pack(pady=10)
        
        log = tk.Text(master, height=8, width=50)
        hist = "\n".join([f"{c['fecha']}: {c['nota']}" for c in paciente.historial])
        log.insert("1.0", hist if hist else "Sin historial."); log.config(state="disabled"); log.pack()

        tk.Label(master, text="Nueva nota:").pack()
        nota = tk.Entry(master, width=50); nota.pack(pady=5)

        tk.Button(master, text="Guardar Nota", bg="green", fg="white", 
                  command=lambda: self.save(app, paciente, nota.get())).pack(pady=10)
        tk.Button(master, text="Volver", command=lambda: app.cambiar_vista(VistaListadoPacientes)).pack()

    def save(self, app, paciente, texto):
        if texto:
            paciente.agregar_consulta(datetime.now().strftime("%d/%m/%Y"), texto)
            app.actualizar_persistencia()
            app.cambiar_vista(VistaListadoPacientes)

if __name__ == "__main__":
    root = tk.Tk()
    AplicacionMedico(root)
    root.mainloop()