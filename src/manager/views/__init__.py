from pydantic import BaseModel


class ErrorContent(BaseModel):
    detail: str
    key: str
