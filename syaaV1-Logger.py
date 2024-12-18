import logging
from config import Config

def setup_logger():
    logger = logging.getLogger("PhantomExploit")
    logger.setLevel(Config.LOG_LEVEL)
    
    formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
    
    file_handler = logging.FileHandler("phantom_exploit.log")
    file_handler.setFormatter(formatter)
    logger.addHandler(file_handler)
    
    if Config.DEBUG:
        console_handler = logging.StreamHandler()
        console_handler.setFormatter(formatter)
        logger.addHandler(console_handler)
    
    return logger

logger = setup_logger()

