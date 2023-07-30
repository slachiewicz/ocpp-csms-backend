from __future__ import annotations

from loguru import logger
from pydantic import BaseModel

import manager.services.charge_points as service
from charge_point_node.fields import EventName
from charge_point_node.models.base import BaseEvent
from manager.views.charge_points import StatusCount


class ConnectionMetaData(BaseModel):
    count: StatusCount


class SSEEventData(BaseModel):
    charge_point_id: str
    name: str
    meta: ConnectionMetaData


class SSEEvent(BaseModel):
    data: SSEEventData
    event: str = "message"


class Redactor:

    async def prepare_event(self, event: BaseEvent) -> SSEEvent:
        meta = {}
        # Note: there is a list ALLOWED_SERVER_SIDE_EVENTS in the settings
        if event.name in [EventName.NEW_CONNECTION, EventName.LOST_CONNECTION]:
            logger.info(f"Start preparing 'connection' event = {event}")
            counts = await service.get_statuses_counts()
            meta = ConnectionMetaData(
                count=StatusCount(**counts)
            )

        data = SSEEventData(
            charge_point_id=event.charge_point_id,
            name=event.name.value,
            meta=meta
        )
        return SSEEvent(data=data)
