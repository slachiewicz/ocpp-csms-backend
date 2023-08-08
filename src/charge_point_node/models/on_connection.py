from charge_point_node.models.base import BaseEvent
from core.fields import ActionName


class OnConnectionEvent(BaseEvent):
    action: ActionName = ActionName.NEW_CONNECTION


class LostConnectionEvent(BaseEvent):
    action: ActionName = ActionName.LOST_CONNECTION
