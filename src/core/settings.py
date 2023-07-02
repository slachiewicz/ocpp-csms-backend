import os

from loguru import logger

DEBUG = os.environ.get("DEBUG", "0") == "1"
WS_SERVER_PORT = int(os.environ["WS_SERVER_PORT"])

logger.add("csms.log", enqueue=True, backtrace=True,
           diagnose=DEBUG, format="{time} - {level} - {message}",
           rotation="10 MB", level="INFO")