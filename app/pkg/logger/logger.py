import logging
from logging.handlers import RotatingFileHandler
from pathlib import Path

from app.pkg.settings import settings


LOG_FORMAT = "%(asctime)s - %(levelname)s - %(name)s - %(filename)s - %(funcName)s - %(lineno)d - %(message)s"


def get_file_handler(file_name) -> RotatingFileHandler:
    Path(file_name).absolute().parent.mkdir(exist_ok=True, parents=True)
    file_handler = RotatingFileHandler(
        filename=file_name,
        maxBytes=5242880,
        backupCount=10,
    )
    file_handler.setFormatter(logging.Formatter(LOG_FORMAT))
    return file_handler


def get_stream_handler() -> logging.StreamHandler:
    stream_handler = logging.StreamHandler()
    stream_handler.setFormatter(logging.Formatter(LOG_FORMAT))
    return stream_handler


def get_logger(name) -> logging.Logger:
    logger = logging.getLogger(name)
    file_path = str(
        Path().cwd().joinpath(settings.LOGGER_DIR_PATH_INTERNAL, "logs.log"),
    )
    if not logger.hasHandlers():
        logger.addHandler(get_file_handler(file_name=file_path))
        logger.addHandler(get_stream_handler())
        logger.setLevel(settings.LOGGER_LEVEL)
    return logger
