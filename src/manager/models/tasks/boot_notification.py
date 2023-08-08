from ocpp.v201.enums import RegistrationStatusType, Action

from manager.models.tasks.base import BaseTask


class BootNotificationTask(BaseTask):
    current_time: str
    interval: int
    status: RegistrationStatusType
    action: Action = Action.BootNotification
