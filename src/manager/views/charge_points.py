from __future__ import annotations

from datetime import datetime

from pydantic import BaseModel

from manager.fields import ChargePointStatus
from manager.views.locations import SimpleLocation


class ChargePointCommonView(BaseModel):
    class Config:
        orm_mode = True


class ChargePointUpdateStatusView(ChargePointCommonView):
    status: ChargePointStatus


class StatusCount(BaseModel):
    available: int
    offline: int
    reserved: int
    charging: int


class SimpleChargePoint(BaseModel):
    id: str
    status: ChargePointStatus
    model: str
    updated_at: datetime | None = None
    location: SimpleLocation

    class Config:
        orm_mode = True
