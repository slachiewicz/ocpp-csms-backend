import json

from aio_pika.abc import AbstractIncomingMessage
from loguru import logger

from charge_point_node.fields import EventName
from charge_point_node.models.on_connection import OnConnectionEvent
from manager.fields import ChargePointStatus
from manager.services.charge_points import update_charge_point_status


async def process_event(message: AbstractIncomingMessage) -> None:
    async with message.process():
        data = json.loads(message.body.decode())
        event_name = data["name"]

        event = {
            EventName.NEW_CONNECTION.value: OnConnectionEvent
        }[event_name](**data)

        logger.info(f"Got event from charge point node (event={event})")

        if event.name is EventName.NEW_CONNECTION:
            await update_charge_point_status(
                charge_point_id=event.charge_point_id,
                status=ChargePointStatus.ONLINE
            )
