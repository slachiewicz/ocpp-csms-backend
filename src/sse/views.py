from __future__ import annotations

from typing import Dict

from pydantic import BaseModel, validator, ValidationError

from charge_point_node.fields import EventName
from charge_point_node.models.base import BaseEvent


class StatusCount(BaseModel):
    online: int
    offline: int
    reserved: int

    @validator("online", "offline", "reserved")
    @classmethod
    def greater_or_equal_to_zero(cls, value):
        if value >= 0:
            return value
        raise ValidationError("The value should be equal or greater than zero.")


class OnConnectionMetaData(BaseModel):
    count: StatusCount


class BootNotificationMetaData(BaseModel):
    last_health: str


class BaseData(BaseModel):
    charge_point_id: str
    name: str
    meta: OnConnectionMetaData | \
          BootNotificationMetaData


class BaseSSE(BaseModel):
    data: BaseData
    event: str = "message"


counter = []


class Redactor:

    async def _prepare_new_connection_event(self):
        # TODO: temp dummy code for a sample ################
        counter.append(1)
        online = len(counter)
        offline = 25 - online
        reserved = 5
        ##################################
        return OnConnectionMetaData(
            count=StatusCount(
                online=online,
                offline=offline,
                reserved=reserved
            )
        )

    async def prepare_event(self, event: BaseEvent) -> Dict:
        meta = {}
        if event.name is EventName.NEW_CONNECTION:
            meta = await self._prepare_new_connection_event()

        data = BaseData(
            charge_point_id=event.charge_point_id,
            name=event.name.value,
            meta=meta
        )
        return BaseSSE(data=data).dict()
