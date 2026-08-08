import logging
import os
from logging.handlers import RotatingFileHandler

def configure_logging():
    log_file_name = "app.log"
    rotating_handler = RotatingFileHandler(
    log_file_name,
    maxBytes=5 * 1024 * 1024,
    backupCount=3,
    delay=True
    )

    log_directory = "logs"
    log_full_path = os.path.join(log_directory, log_file_name)
    os.makedirs(log_directory, exist_ok=True)
    logging.basicConfig(
    # TODO: Apply config for log level
    level=logging.INFO,
    format="%(levelname)s: %(asctime)s - %(name)s - %(message)s", 
    handlers=[
        logging.StreamHandler(),
        logging.FileHandler(log_full_path, mode="a"),
        rotating_handler,
    ],)
    logger = logging.getLogger(__name__)
    
    return logger