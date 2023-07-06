from __future__ import annotations

from typing import Dict

from pydantic import BaseModel

from charge_point_node.fields import EventName
from charge_point_node.models.base import BaseEvent


class OnConnectionMetaData(BaseModel):
    entire_online_count: int


class BootNotificationMetaData(BaseModel):
    last_health: str


class BaseData(BaseModel):
    charge_point_id: str
    name: str
    meta: OnConnectionMetaData | \
          BootNotificationMetaData


class BaseSSE(BaseModel):
    data: BaseData


counter = []


class Redactor:

    async def _prepare_new_connection_event(self):
        # TODO: temp code ################
        counter.append(1)
        entire_online_count = len(counter)
        ##################################
        return OnConnectionMetaData(
            entire_online_count=entire_online_count
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
