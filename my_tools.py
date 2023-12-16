import logging

def get_a_logger(file="log.log",**kwargs) -> logging.Logger:
    # Create a custom logger
    logger = logging.getLogger(__name__)
    # Create handlers
    f_handler = logging.FileHandler(file)
    f_handler.setLevel(logging.DEBUG if "level" not in kwargs else kwargs["level"] )
    # Create formatters and add it to handlers
    f_format = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
    f_handler.setFormatter(f_format)
    # Add handlers to the logger
    logger.addHandler(f_handler)
    logger.setLevel(logging.DEBUG if "level" not in kwargs else kwargs["level"] )
    return logger

if __name__ == "__main__":
    logger = get_a_logger()
    logger.debug("Hola")
    logger.warning('This is a warning')
    logger.error('This is an error')