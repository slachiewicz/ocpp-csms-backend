from functools import wraps
from typing import Callable

from loguru import logger

from charge_point_node.fields import EventName
from charge_point_node.models.base import BaseEvent
from charge_point_node.models.on_connection import OnConnectionEvent
from sse import sse_publisher


def prepare_event(func) -> Callable:
    @wraps(func)
    async def wrapper(data):
        event = {
            EventName.NEW_CONNECTION.value: OnConnectionEvent
        }[data["name"]](**data)
        return await func(event)

    return wrapper


@prepare_event
@sse_publisher.publish
async def process_event(event: BaseEvent) -> BaseEvent:
    logger.info(f"Got event from charge point node (event={event})")

    # if event.name is EventName.NEW_CONNECTION:
    #     await update_charge_point(
    #         charge_point_id=event.charge_point_id,
    #         data=ChargePointUpdateStatusView(status=ChargePointStatus.AVAILABLE)
    #     )

    return event
