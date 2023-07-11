from enum import Enum


class ChargePointStatus(str, Enum):
    AVAILABLE = "available"
    OFFLINE = "offline"
    RESERVED = "reserved"
    CHARGING = "charging"
