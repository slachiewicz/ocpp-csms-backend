import os

from loguru import logger

from charge_point_node.fields import EventName

DEBUG = os.environ.get("DEBUG") == "1"

RABBITMQ_PORT = os.environ["RABBITMQ_PORT"]
RABBITMQ_UI_PORT = os.environ["RABBITMQ_UI_PORT"]
RABBITMQ_USER = os.environ["RABBITMQ_USER"]
RABBITMQ_PASS = os.environ["RABBITMQ_PASS"]
RABBITMQ_HOST = os.environ["RABBITMQ_HOST"]

logger.add(
    "csms.log",
    enqueue=True,
    backtrace=True,
    diagnose=DEBUG,
    format="{time} - {level} - {message}",
    rotation="50 MB",
    level="INFO"
)

WS_SERVER_PORT = int(os.environ["WS_SERVER_PORT"])

EVENTS_QUEUE_NAME = os.environ["EVENTS_QUEUE_NAME"]
TASKS_QUEUE_NAME = os.environ["TASKS_QUEUE_NAME"]

ALLOWED_SSE_EVENTS = [
    EventName.NEW_CONNECTION
]
