import requests
import os, json
from dotenv import load_dotenv
load_dotenv()
import my_tools
USER                    = os.getenv('USER_BUHO_LEGAL')
PASSWORD                = os.getenv('PASSWORD')
API_BASE                = os.getenv('API_BASE')
BUHO_CREDENTIALS        = os.getenv('BUHO_CREDENTIALS')
API_CREATE_USER         = os.getenv('API_CREATE_USER')
API_GET_TOKEN           = os.getenv('API_GET_TOKEN')
API_GET_ESTADOS         = os.getenv('API_GET_ESTADOS')
API_BUSQUEDA_EXPEDIENTE = os.getenv('API_BUSQUEDA_EXPEDIENTE')
API_HIST_BUSQUEDAS      = os.getenv("API_HIST_BUSQUEDAS")
API_VALIDAR_CURP        = os.getenv("API_VALIDAR_CURP")
API_GET_CEDULAS         = os.getenv("API_GET_CEDULAS")

ERROR_MESSAGE = f"Error al enviar request."

logger              = my_tools.get_a_logger()

class BuhoLegal:
    def __init__(self, user = USER, password = PASSWORD):
        logger.debug("Creando Fachada BuhoLegal...")
        self.user = user
        self.password = password
        self.__token = None

    def __get_token(self) -> None:
        logger.debug(f"Recuperando Token para conectarme a la API Buho legal: {API_GET_TOKEN}")
        credenciales = { 'username' : self.user, 'password' : self.password}
        logger.debug(f"credenciales: {credenciales}")
        respose = requests.post(API_GET_TOKEN, data=credenciales) 
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

    def create_user(self, **kwargs):
        logger.debug(f"Creando usuario hacia la API: {API_CREATE_USER}")
        headers = { 'Authorization' : 'Token ' + self.__token }
        """
        data = { 'username' : 'maik69', 'password' : '3jemploPassword', 'confirm_password' : '3jemploPassword', 'description' : 'Mi compa el chueco' }
        """
        data = { 'username' : 'maik69', 'password' : '3jemploPassword', 'confirm_password' : '3jemploPassword', 'description' : 'Mi compa el chueco' }  
        respose = requests.post(API_CREATE_USER, data=data, headers=headers)
        logger.debug(f"response: {respose.json()}")
        return respose.json()
    
    
    def get_estados(self):
        """
        El objetivo de esta funcionalidad es permitir a los usuarios conocer 
        las abreviaturas que se utilizan para referirse a cada estado a la 
        hora de realizar una búsqueda.
        """
        logger.debug(f"Obteniendo estados...")
        try:
            response = requests.get(API_GET_ESTADOS, headers = {'Authorization':'Token ' + self.__token})
            if response.status_code == 200:
                logger.info(f"Estados recuperados!")
                return response.json()
            else:
                logger.error(f"No se pueden obtener los estados.")
                raise Exception(f"No se pueden obtener los estados.")
        except:
            logger.error(ERROR_MESSAGE)
            raise Exception(ERROR_MESSAGE)
        
        
    def busqueda(self):
        logger.debug(f"Realizando búsqueda de expedientes...")
        PARAMS = {}
        PARAMS['nombre'] = 'juan'
        PARAMS['paterno'] = 'mengano'
        PARAMS['materno'] = 'sultano'
        PARAMS['persona'] = 'fisica'
        PARAMS['estado'] = 'AS' # AS se refiere a Aguascalientes. PARAMS['detalle'] = True
        PARAMS['detalle'] = True
        PARAMS['fecha_inicio'] = '01-01-2019' 
        PARAMS['fecha_fin'] = '01-06-2020' 
        PARAMS['curp'] = 'ASDF801332GYBHQL00'
        try:
            response = requests.get(API_BUSQUEDA_EXPEDIENTE, headers = {'Authorization':'Token ' + self.__token}, params=PARAMS)
            if response.status_code == 200:
                logger.info("Obteniendo expediente!")
                return response.json()
            else:
                logger.error(f"No se puede obtener el expediente.")
                raise Exception(f"No se puede obtener el expediente.")
        except:
            logger.error(ERROR_MESSAGE)
            raise Exception(ERROR_MESSAGE)
            
    def get_busquedas(self):
        logger.debug(f"Consultando el historial de busquedas...")
        PARAMS = {}
        PARAMS['fecha_inicio'] = '01-01-2019' 
        PARAMS['fecha_fin'] = '01-06-2020'
        try:
            response = requests.get(API_HIST_BUSQUEDAS, headers = {'Authorization':'Token ' + self.__token}, params=PARAMS)
            if response.status_code == 200:
                logger.info(f"Obteniendo historial de busquedas!")
                return response.json()
            else:
                logger.error(f"No se puede obtener el historial de busquedas.")
                raise Exception(f"No se puede obtener el historial de busquedas.")
        except:
            logger.error(ERROR_MESSAGE)
            raise Exception(ERROR_MESSAGE)
        
    def validar_curp(self):
        logger.debug(f"Validando CURP..")
        try:
            response = requests.get(API_VALIDAR_CURP, headers = {'Authorization':'Token ' + self.__token}, params={'curp':'VIAL885764656465'})
            if response.status_code == 200:
                logger.info(f"CURP validada!")
                return response.json()
            else:
                logger.error(f"No se puede validar la CURP.")
                raise Exception(f"No se puede validar la CURP.")
        except:
            logger.error(ERROR_MESSAGE)
            raise Exception(ERROR_MESSAGE)
        
    def get_cedulas(self):
        logger.debug(f"Obteniendo cedulas profesionales..")
        PARAMS = {'nombre' : 'Juan', 'paterno' : 'Mengano', 'materno' : 'Sultano'}
        try:
            response = requests.get(API_GET_CEDULAS, headers = {'Authorization':'Token ' + self.__token}, params=PARAMS)
            if response.status_code == 200:
                logger.info(f"Cedulas obtenidas!")
                return response.json()
            else:
                logger.error(f"No se pueden obtener las cedulas.")
                raise Exception(f"No se pueden obtener las cedulas.")
        except:
            logger.error(ERROR_MESSAGE)
            raise Exception(ERROR_MESSAGE)
                
                
            
        
        
    
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