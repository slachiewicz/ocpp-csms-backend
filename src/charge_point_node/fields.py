from enum import Enum


class EventName(str, Enum):
    NEW_CONNECTION = "new_connection"