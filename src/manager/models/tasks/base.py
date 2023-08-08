from ocpp.v201.enums import Action
from pydantic import BaseModel

from core.fields import ActionName
from core.settings import TASKS_QUEUE_NAME, REGULAR_MESSAGE_PRIORITY


class BaseTask(BaseModel):
    message_id: str
    charge_point_id: str
    action: ActionName | Action
    target_queue: str = TASKS_QUEUE_NAME
    priority: int = REGULAR_MESSAGE_PRIORITY
