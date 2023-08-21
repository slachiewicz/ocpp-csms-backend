import re
from http import HTTPStatus

from fastapi import HTTPException
from sqlalchemy.exc import IntegrityError
from starlette import status
from starlette.requests import Request
from starlette.responses import JSONResponse

from manager import app
from manager.views import ErrorContent


class Forbidden(HTTPException):
    def __init__(self, *args, **kwargs):
        super().__init__(
            status_code=HTTPStatus.FORBIDDEN,
            *args,
            **kwargs
        )


class BadRequest(HTTPException):
    def __init__(self, *args, **kwargs):
        super().__init__(status_code=HTTPStatus.BAD_REQUEST,
                         *args,
                         **kwargs)


@app.exception_handler(IntegrityError)
async def unique_violation_exception_handler(request: Request, exc: IntegrityError):
    pattern = re.compile(r"Key \((.*?)\)=\((.*?)\) (.*)")
    name, value, reason = pattern.search(exc.args[0]).groups()
    context = ErrorContent(detail=f"'{value}' {reason}", key=name)
    return JSONResponse(
        status_code=status.HTTP_409_CONFLICT,
        content=context.dict(),
    )
