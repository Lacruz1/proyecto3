import json
import os
import logging
from principal.modelos import Doctor, Paciente

class GestorDatos:
    def __init__(self, archivo="datos.json"):
        self.archivo = archivo

    def guardar(self, doctor, pacientes):
        # transforma los datos para que le json los puieda guardar
        try:
            datos = {
                "doctor": {
                    "nombre": doctor.nombre,
                    "edad": doctor.edad,
                    "usuario": doctor.usuario,
                    "clave": doctor.clave
                } if doctor else None,
                "pacientes": [
                    {
                        "nombre": p.nombre, "edad": p.edad,
                        "padecimientos": p.padecimientos, "peso": p.peso,
                        "historial": p.historial
                    } for p in pacientes
                ]
            }
            with open(self.archivo, "w") as f:
                json.dump(datos, f, indent=4)
        except Exception as e:
            logging.exception(f"Error al guardar datos: {e}")
            raise e

    def cargar(self):
        # carga el json, y recontruye los datos para que el programa los lea
        if not os.path.exists(self.archivo):
            return None, []

        try:
            with open(self.archivo, "r") as f:
                datos = json.load(f)
                
                doctor = None
                if datos.get("doctor"):
                    d = datos["doctor"]
                    doctor = Doctor(d["nombre"], d["edad"], d["usuario"], d["clave"])
                
                pacientes = []
                for p in datos.get("pacientes", []):
                    nuevo = Paciente(p["nombre"], p["edad"], p["padecimientos"], p["peso"], p.get("historial", []))
                    pacientes.append(nuevo)
                
                return doctor, pacientes
        except Exception:
            return None, []