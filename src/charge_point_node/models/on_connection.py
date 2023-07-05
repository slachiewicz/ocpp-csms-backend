from charge_point_node.fields import EventName
from charge_point_node.models.base import BaseEvent


class OnConnectionEvent(BaseEvent):
    charge_point_id: str
    name: EventName = EventName.NEW_CONNECTION
