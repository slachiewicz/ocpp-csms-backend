import asyncio

from fastapi import FastAPI

from core.queue.consumer import start_consume
from core.settings import EVENTS_QUEUE_NAME
from manager.controllers.status import status_router
from manager.services.events import process_event

app = FastAPI()


@app.on_event("startup")
async def startup():
    asyncio.ensure_future(
        start_consume(queue_name=EVENTS_QUEUE_NAME, on_message=process_event)
    )


app.include_router(status_router)
