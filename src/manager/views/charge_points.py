from __future__ import annotations

from datetime import datetime
from typing import List

from pydantic import BaseModel

from core.fields import ChargePointStatus
from manager.views import PaginationView
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


class PaginatedChargePointsView(BaseModel):
    items: List[SimpleChargePoint]
    pagination: PaginationView
