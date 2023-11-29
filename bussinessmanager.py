import requests
import os
from dotenv import load_dotenv
load_dotenv()

USER        = os.getenv('USER_BUHO_LEGAL')
PASSWORD    = os.getenv('PASSWORD')
API_BASE    = os.getenv('API_BASE')

class BuhoLegal:
    def __init__(self, user = USER, password = PASSWORD):
        self.user = user
        self.password = password
        self.token = None

    def get_token(self):
        credenciales = { 'username' : self.user, 'password' : self.password}
        respose = requests.post(f'{API_BASE}/apikey/', data=credenciales) 
        if respose.status_code == 200:
            token = respose.json()['token']
            print(token)
            self.token = token
        else:
            raise Exception("No pude obtener el token necesario")
        return token

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