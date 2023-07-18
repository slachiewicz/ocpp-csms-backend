from enum import Enum


class TaskName(str, Enum):
    pass


class ChargePointStatus(str, Enum):
    AVAILABLE = "available"
    OFFLINE = "offline"
    RESERVED = "reserved"
    CHARGING = "charging"
