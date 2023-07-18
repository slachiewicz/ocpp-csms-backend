from pydantic import BaseModel


class ChargePointAuthView(BaseModel):
    password: str
