import asyncio

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from core.queue.consumer import start_consume
from core.settings import EVENTS_QUEUE_NAME
from manager.controllers.charge_points import charge_points_router
from manager.controllers.status import status_router
from manager.services.events import process_event
from sse.controllers import stream_router

app = FastAPI()

origins = ["*"]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.on_event("startup")
async def startup():
    asyncio.ensure_future(
        start_consume(queue_name=EVENTS_QUEUE_NAME, on_message=process_event)
    )


app.include_router(status_router)
app.include_router(stream_router)
app.include_router(charge_points_router)
