from charge_point_node.fields import EventName
from charge_point_node.models.base import BaseEvent


class OnConnectionEvent(BaseEvent):
    name: EventName = EventName.NEW_CONNECTION


class LostConnectionEvent(BaseEvent):
    name: EventName = EventName.LOST_CONNECTION
