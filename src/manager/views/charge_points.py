from pydantic import BaseModel

from manager.fields import ChargePointStatus


class ChargePointCommonView(BaseModel):
    class Config:
        orm_mode = True


class ChargePointUpdateStatusView(ChargePointCommonView):
    status: ChargePointStatus
