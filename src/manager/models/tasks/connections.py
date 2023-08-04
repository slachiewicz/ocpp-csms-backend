from manager.fields import TaskName
from manager.models.tasks.base import BaseTask


class DisconnectTask(BaseTask):
    charge_point_id: str
    name: TaskName = TaskName.DISCONNECT
