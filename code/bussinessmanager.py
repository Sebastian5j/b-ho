import requests
import os
from dotenv import load_dotenv
load_dotenv()

MY_ENV_VAR = os.getenv('MY_ENV_VAR')

class BuhoLegal:
    def get_token(self):
        credenciales = { 'username' : 'sebastianqjuarez@gmail.com', 'password' : 'p4r4BuhoLegal' }
        respose = requests.post('https://api.buholegal.com/apikey/', data=credenciales) 
        if respose.status_code == 200:
            token = respose.json()['token']
            print(token)
            self.token = token
        else:
            raise Exception("No pude obtener el token necesario")

class Manager:
    
    def __init__(self, buho: BuhoLegal) -> None:
        self._buho = buho or BuhoLegal()

    def get_token(self) -> str:
        token = self._buho.get_token()
        return token
    
def client_code(facade: Manager) -> None:
    facade.get_token()


if __name__ == "__main__":
    # The client code may have some of the subsystem's objects already created.
    # In this case, it might be worthwhile to initialize the Facade with these
    # objects instead of letting the Facade create new instances.
    buho = BuhoLegal()
    manager = Manager(buho= buho)
    client_code(manager)