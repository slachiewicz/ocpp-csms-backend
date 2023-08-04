from http import HTTPStatus

from fastapi import HTTPException


class Forbidden(HTTPException):
    def __init__(self, *args, **kwargs):
        super().__init__(
            status_code=HTTPStatus.FORBIDDEN,
            *args,
            **kwargs
        )
