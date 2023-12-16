import requests
import os, json
from dotenv import load_dotenv
load_dotenv()
import my_tools
USER                = os.getenv('USER_BUHO_LEGAL')
PASSWORD            = os.getenv('PASSWORD')
API_BASE            = os.getenv('API_BASE')
BUHO_CREDENTIALS    = os.getenv('BUHO_CREDENTIALS')

logger              = my_tools.get_a_logger()

class BuhoLegal:
    def __init__(self, user = USER, password = PASSWORD):
        logger.debug("Creando Fachada BuhoLegal...")
        self.user = user
        self.password = password
        self.__token = None

    def __get_token(self) -> None:
        logger.debug("Recuperando Token para conectarme a la API Buho legal")
        credenciales = { 'username' : self.user, 'password' : self.password}
        respose = requests.post(f'{API_BASE}/apikey/', data=credenciales) 
        if respose.status_code == 200:
            logger.debug("Token recuperado!")
            token = respose.json()['token']
            self.__token = token
        else:
            logger.error(f"No se autentico correctamente con la API: {respose}")
            raise Exception("No pude obtener el token necesario")
    
    def connect(self):
        logger.debug("Conectando a Buho Legal...")
        self.__get_token()
        logger.debug(f"Guardando el token...")
        data = {"token": self.__token}
        with open(BUHO_CREDENTIALS, 'w') as f:
            json.dump(data, f)
        logger.debug("Guardado!")

        logger.debug("Conectado!")

    def create_user(self):
        headers = { 'Authorization' : 'Token ' + self.__token }
        data = { 'username' : 'maik69', 'password' : '3jemploPassword', 'confirm_password' : '3jemploPassword', 'description' : 'Mi compa el chueco' }
        respose = requests.post('https://api.buholegal.com/crear_usuario/', data=data, headers=headers)
        logger.debug(f"response: {respose.json()}")
        return respose.json()
    
class Manager:
    
    def __init__(self, buho: BuhoLegal) -> None:
        self._buho = buho or BuhoLegal()

    def create_user(self) -> str:
        self._buho.connect()
        self._buho.create_user()
    
def client_code(facade: Manager) -> None:
    facade.create_user()
    


if __name__ == "__main__":
    # The client code may have some of the subsystem's objects already created.
    # In this case, it might be worthwhile to initialize the Facade with these
    # objects instead of letting the Facade create new instances.
    buho = BuhoLegal()
    manager = Manager(buho= buho)
    client_code(manager)