import os

from loguru import logger

from charge_point_node.fields import EventName

DEBUG = os.environ.get("DEBUG") == "1"

RABBITMQ_PORT = os.environ["RABBITMQ_PORT"]
RABBITMQ_UI_PORT = os.environ["RABBITMQ_UI_PORT"]
RABBITMQ_USER = os.environ["RABBITMQ_USER"]
RABBITMQ_PASS = os.environ["RABBITMQ_PASS"]
RABBITMQ_HOST = os.environ["RABBITMQ_HOST"]

DB_NAME = os.environ["DB_NAME"]
DB_PASSWORD = os.environ["DB_PASSWORD"]
DB_PORT = int(os.environ["DB_PORT"])
DB_USER = os.environ["DB_USER"]
DB_HOST = os.environ["DB_HOST"]

DATABASE_ASYNC_URL = f"postgresql+asyncpg://{DB_USER}:{DB_PASSWORD}@{DB_HOST}/{DB_NAME}"
DATABASE_SYNC_URL = f"postgresql://{DB_USER}:{DB_PASSWORD}@{DB_HOST}/{DB_NAME}"

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

HTTP_SERVER_HOST = os.environ["HTTP_SERVER_HOST"]
HTTP_SERVER_PORT = int(os.environ["HTTP_SERVER_PORT"])

EVENTS_QUEUE_NAME = os.environ["EVENTS_QUEUE_NAME"]
TASKS_QUEUE_NAME = os.environ["TASKS_QUEUE_NAME"]

ALLOWED_SERVER_SIDE_EVENTS = [
    EventName.NEW_CONNECTION,
    EventName.LOST_CONNECTION
]

DATETIME_FORMAT = "YYYY-MM-DD HH:mm:ss"
LOCK_FOLDER = "/tmp/lock"
