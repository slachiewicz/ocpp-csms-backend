from core.fields import ActionName
from manager.models.tasks.base import BaseTask


class DisconnectTask(BaseTask):
    charge_point_id: str
    name: ActionName = ActionName.DISCONNECT

