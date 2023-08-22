from pydantic import BaseModel


class ErrorContent(BaseModel):
    detail: str
    key: str


class PaginationView(BaseModel):
    current_page: int
    last_page: int
    total: int