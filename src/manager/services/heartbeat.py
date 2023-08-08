from charge_point_node.models.base import BaseEvent
from core.utils import get_utc_as_string
from manager.models.tasks.heartbeat import HeartbeatTask


async def process_heartbeat(event: BaseEvent) -> HeartbeatTask:
    # Do some logic here

    return HeartbeatTask(
        message_id=event.message_id,
        charge_point_id=event.charge_point_id,
        current_time=get_utc_as_string()
    )
