from enum import Enum


class TaskName(str, Enum):
    DISCONNECT = "disconnect"


class ChargePointStatus(str, Enum):
    AVAILABLE = "available"
    OFFLINE = "offline"
    RESERVED = "reserved"
    CHARGING = "charging"
