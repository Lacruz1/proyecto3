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

    def test_agregar_consulta_paciente(self):
        #para ver si el historiual esta vacio
        self.assertEqual(len(self.paciente_prueba.historial), 0)
        
        #se agrega una consulta
        self.paciente_prueba.agregar_consulta("20/05/2024", "paciente con fiebre")
        
        #ahora se ve si hay una consulta 
        #y luego vemos si el texto es ek mismo
        self.assertEqual(len(self.paciente_prueba.historial), 1)
        self.assertEqual(self.paciente_prueba.historial[0]["nota"], "paciente con fiebre")

if __name__ == "__main__":
    unittest.main()