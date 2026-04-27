class ErrorDeLogin(Exception):
    """Excepción personalizada para errores de credenciales."""
    pass

class Autenticacion:
    def __init__(self, usuario, clave):
        self.usuario = usuario
        self.clave = clave

    def Validar_acceso(self, intento_usuario, intento_clave):
        if intento_usuario == self.usuario and intento_clave == self.clave:
            return True 
        raise ErrorDeLogin("Usuario o clave incorrectos")