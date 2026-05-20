import unittest
from principal.autenticacion import Autenticacion, ErrorDeLogin
from principal.modelos import Paciente, Doctor

#esto se usa para inicializar las pruebas
class TestSistemaMedico(unittest.TestCase):
    def setUp(self):
        self.auth_prueba = Autenticacion("admin", "1234")
        self.paciente_prueba = Paciente("juan", 25, "gripe", 70.8)

    def test_login_exitoso(self):
        #si los datos son validos devuelve true
        self.assertTrue(self.auth_prueba.Validar_acceso("admin", "1234"))

    def test_login_fallido(self):
        #verifica que si la clave es la correcta
        #si no lanza error
        with self.assertRaises(ErrorDeLogin):
            self.auth_prueba.Validar_acceso("admin", "clave_erronea")

if __name__ == "__main__":
    unittest.main()