import logging
import os

from fastapi.logger import logger as fastapi_logger

__api_name__ = "api"

# check if log dir exists
if not os.path.exists("logs"):
    os.makedirs("logs")

_log_path = os.path.join("logs", __api_name__ + ".log")


def _rotating_handler():
    formatter = logging.Formatter("%(asctime)s %(levelname)s %(name)s | %(message)s")

    file_handler = logging.FileHandler(filename=_log_path, mode="a")
    file_handler.setLevel(logging.DEBUG)
    file_handler.setFormatter(formatter)

    # add to root
    root_logger = logging.getLogger()
    root_logger.addHandler(file_handler)

    return file_handler


def _get_cli_logger(file_handler):
    # get handler from uvicorn
    uvicorn_logger = logging.getLogger("uvicorn")
    handler = uvicorn_logger.handlers[0]

    logger = logging.getLogger(__api_name__)
    logger.handlers = [handler]
    logger.addHandler(file_handler)

    logger.setLevel(uvicorn_logger.level)

    return logger


def _configure_fastapi(handlers):
    fastapi_logger.handlers = handlers


# root logging
rfhandler = _rotating_handler()

# get asteroid logger
logger = _get_cli_logger(rfhandler)

# configure fastapi
_configure_fastapi(logger.handlers)
