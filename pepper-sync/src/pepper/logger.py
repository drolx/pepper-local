import logging
from fastapi.logger import logger as fastapi_logger
from logging.handlers import RotatingFileHandler

def configure_logging():
    log_file_name = "app.log"
    rotating_handler = RotatingFileHandler(
    log_file_name, maxBytes=5 * 1024 * 1024, backupCount=3
    )

    logging.basicConfig(
    # TODO: Apply config for log level
    level=logging.INFO,
    format="%(levelname)s: %(asctime)s - %(name)s - %(message)s", 
    handlers=[
        logging.StreamHandler(),
        logging.FileHandler(log_file_name, mode="a"),
        rotating_handler,
    ],)
    fastapi_logger.setLevel(logging.INFO)
    fastapi_logger.handlers = logging.getLogger().handlers

    return fastapi_logger
