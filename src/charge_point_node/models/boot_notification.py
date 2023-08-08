from ocpp.v201.enums import Action

from charge_point_node.models.base import BaseEvent


class BootNotificationEvent(BaseEvent):
    action: Action = Action.BootNotification
