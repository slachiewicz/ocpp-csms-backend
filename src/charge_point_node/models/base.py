from pydantic import BaseModel

from charge_point_node.fields import EventName
from core.settings import EVENTS_QUEUE_NAME


class BaseEvent(BaseModel):
    name: EventName
    target_queue: str = EVENTS_QUEUE_NAME
