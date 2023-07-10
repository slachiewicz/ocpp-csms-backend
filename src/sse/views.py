from __future__ import annotations

from pydantic import BaseModel, validator, ValidationError

from charge_point_node.fields import EventName
from charge_point_node.models.base import BaseEvent


class StatusCount(BaseModel):
    available: int
    offline: int
    reserved: int
    charging: int

    @validator("available", "offline", "reserved", "charging")
    @classmethod
    def greater_or_equal_to_zero(cls, value):
        if value >= 0:
            return value
        raise ValidationError("The value should be equal or greater than zero.")


class OnConnectionMetaData(BaseModel):
    count: StatusCount


class BootNotificationMetaData(BaseModel):
    last_health: str


class SSEEventData(BaseModel):
    charge_point_id: str
    name: str
    meta: OnConnectionMetaData | \
          BootNotificationMetaData


class SSEEvent(BaseModel):
    data: SSEEventData
    event: str = "message"


total_stations = 25
counter = []


class Redactor:

    async def _prepare_new_connection_event(self):
        # TODO: temp dummy code for a sample ################
        counter.append(1)
        available = len(counter)
        offline = total_stations - available
        reserved = 5
        charging = 2
        ##################################
        return OnConnectionMetaData(
            count=StatusCount(
                available=available,
                offline=offline,
                reserved=reserved,
                charging=charging
            )
        )

    async def prepare_event(self, event: BaseEvent) -> SSEEvent:
        meta = {}
        if event.name is EventName.NEW_CONNECTION:
            meta = await self._prepare_new_connection_event()

        data = SSEEventData(
            charge_point_id=event.charge_point_id,
            name=event.name.value,
            meta=meta
        )
        return SSEEvent(data=data)
