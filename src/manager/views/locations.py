from pydantic import BaseModel


class SimpleLocation(BaseModel):
    name: str
    city: str

    class Config:
        orm_mode = True
