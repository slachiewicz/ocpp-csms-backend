import json

from pydantic import BaseModel

from charge_point_node.fields import EventName
from core.settings import EVENTS_QUEUE_NAME, REGULAR_MESSAGE_PRIORITY


class BaseEvent(BaseModel):
    charge_point_id: str
    name: EventName
    target_queue: str = EVENTS_QUEUE_NAME
    priority: int = REGULAR_MESSAGE_PRIORITY

    def __str__(self):
        return json.dumps({k: v for k, v in self.dict().items() if k != "password"})
