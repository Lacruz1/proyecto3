import unittest
from principal.autenticacion import Autenticacion, ErrorDeLogin
from principal.modelos import Paciente, Doctor

#esto se usa para inicializar las pruebas
class TestSistemaMedico(unittest.TestCase):
    def setUp(self):
        self.auth_prueba = Autenticacion("admin", "1234")
        self.paciente_prueba = Paciente("juan", 25, "gripe", 70.8)

if __name__ == "__main__":
    unittest.main()