from typing import Dict

from loguru import logger

from charge_point_node.fields import EventName
from charge_point_node.models.base import BaseEvent
from charge_point_node.models.on_connection import OnConnectionEvent
from manager.fields import ChargePointStatus
from manager.services.charge_points import update_charge_point_status
from sse import sse_publisher


@sse_publisher.publish
async def process_event(data: Dict) -> BaseEvent:
    event = {
        EventName.NEW_CONNECTION.value: OnConnectionEvent
    }[data["name"]](**data)

    logger.info(f"Got event from charge point node (event={event})")

    if event.name is EventName.NEW_CONNECTION:
        await update_charge_point_status(
            charge_point_id=event.charge_point_id,
            status=ChargePointStatus.AVAILABLE
        )
    return event
