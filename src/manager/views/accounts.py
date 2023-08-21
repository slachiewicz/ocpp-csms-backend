from pydantic import BaseModel


class CreateAccountView(BaseModel):
    name: str

    class Config:
        orm_mode = True
