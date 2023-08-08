from loguru import logger
from ocpp.v201.call_result import HeartbeatPayload
from ocpp.v201.enums import Action

from charge_point_node.models.heartbeat import HeartbeatEvent
from charge_point_node.router import Router
from core.queue.publisher import publish
from manager.models.tasks.heartbeat import HeartbeatTask

router = Router()


@router.on(Action.Heartbeat)
async def on_heartbeat(
        message_id: str,
        charge_point_id: str,
        **kwargs
):
    logger.info(f"Start accept heartbeat "
                f"(charge_point_id={charge_point_id}, "
                f"message_id={message_id}).")
    event = HeartbeatEvent(
        charge_point_id=charge_point_id,
        message_id=message_id
    )
    await publish(event.json(), to=event.target_queue, priority=event.priority)


@router.out(Action.Heartbeat)
async def respond_heartbeat(task: HeartbeatTask) -> HeartbeatPayload:
    logger.info(f"Start respond heartbeat task={task}).")
    return HeartbeatPayload(current_time=task.current_time)
