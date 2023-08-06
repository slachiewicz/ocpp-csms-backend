from pydantic import BaseModel

from core.settings import TASKS_QUEUE_NAME, REGULAR_MESSAGE_PRIORITY
from manager.fields import TaskName


class BaseTask(BaseModel):
    charge_point_id: str
    name: TaskName
    target_queue: str = TASKS_QUEUE_NAME
    priority: int = REGULAR_MESSAGE_PRIORITY
