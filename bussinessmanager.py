import requests
import os
from dotenv import load_dotenv
load_dotenv()
import my_tools
USER        = os.getenv('USER_BUHO_LEGAL')
PASSWORD    = os.getenv('PASSWORD')
API_BASE    = os.getenv('API_BASE')
logger = my_tools.get_a_logger()

class BuhoLegal:
    def __init__(self, user = USER, password = PASSWORD):
        logger.debug("Creando Fachada BuhoLegal...")
        self.user = user
        self.password = password
        self.token = None

    def get_token(self) -> None:
        logger.debug("Recuperando Token para conectarme a la API Buho legal")
        credenciales = { 'username' : self.user, 'password' : self.password}
        respose = requests.post(f'{API_BASE}/apikey/', data=credenciales) 
        if respose.status_code == 200:
            logger.debug("Token recuperado!")
            token = respose.json()['token']
            self.token = token
        else:
            logger.error(f"No se autentico correctamente con la API: {respose}")
            raise Exception("No pude obtener el token necesario")

class Manager:
    
    def __init__(self, buho: BuhoLegal) -> None:
        self._buho = buho or BuhoLegal()

    def get_token(self) -> str:
        self._buho.get_token()
    
def client_code(facade: Manager) -> None:
    facade.get_token()


if __name__ == "__main__":
    # The client code may have some of the subsystem's objects already created.
    # In this case, it might be worthwhile to initialize the Facade with these
    # objects instead of letting the Facade create new instances.
    buho = BuhoLegal()
    manager = Manager(buho= buho)
    client_code(manager)