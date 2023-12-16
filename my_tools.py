import logging, os
from dotenv import load_dotenv
load_dotenv()

LOG_FILE    = os.environ.get('LOG_FILE')
LOG_LEVEL   = os.environ.get('LOG_LEVEL')

def get_a_logger(file=LOG_FILE,**kwargs) -> logging.Logger:
    # Create a custom logger
    logger = logging.getLogger(__name__)
    # Create handlers
    f_handler = logging.FileHandler(file)
    f_handler.setLevel(logging.INFO if  not LOG_LEVEL  else LOG_LEVEL)
    # Create formatters and add it to handlers
    f_format = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
    f_handler.setFormatter(f_format)
    # Add handlers to the logger
    logger.addHandler(f_handler)
    logger.setLevel(logging.INFO if  not LOG_LEVEL  else LOG_LEVEL)
    return logger

if __name__ == "__main__":
    logger = get_a_logger()
    logger.debug("Hola")
    logger.warning('This is a warning')
    logger.error('This is an error')