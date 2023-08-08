from enum import Enum


class ActionName(str, Enum):
    NEW_CONNECTION = "new_connection"
    LOST_CONNECTION = "lost_connection"
    DISCONNECT = "disconnect"


class ChargePointStatus(str, Enum):
    AVAILABLE = "available"
    OFFLINE = "offline"
    RESERVED = "reserved"
    CHARGING = "charging"
