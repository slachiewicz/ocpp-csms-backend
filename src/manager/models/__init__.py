from pydantic import BaseModel

from core.settings import TASKS_QUEUE_NAME
from manager.fields import TaskName


class BaseTask(BaseModel):
    charge_point_id: str
    name: TaskName
    target_queue: str = TASKS_QUEUE_NAME
