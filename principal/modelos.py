from principal.autenticacion import Autenticacion

class Persona:
    def __init__(self, nombre, edad):
        self.nombre = nombre
        self.edad = edad

class Paciente(Persona):
    def __init__(self, nombre, edad, padecimientos, peso):
        super().__init__(nombre, edad)
        self.padecimientos = padecimientos
        self.peso = peso
        self.historial_citas = []

class Doctor(Persona, Autenticacion):
    def __init__(self, nombre, edad, usuario, clave):
        Persona.__init__(self, nombre, edad)
        Autenticacion.__init__(self, usuario, clave)