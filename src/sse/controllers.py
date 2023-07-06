import asyncio
from functools import wraps
from typing import List, Callable

from fastapi import APIRouter
from sse_starlette.sse import EventSourceResponse
from starlette.requests import Request

from charge_point_node.fields import EventName

ALLOWED_SSE_EVENTS = [
    EventName.NEW_CONNECTION
]

stream_router = APIRouter(tags=["stream"])


class Publisher:
    observers: List["Observer"] = []

    async def ensure_observers(self):
        for observer in self.observers:
            if await observer.request.is_disconnected():
                self.observers.remove(observer)
                del observer

    def publish(self, func) -> Callable:
        @wraps(func)
        async def wrapper(*args, **kwargs):
            event = await func(*args, **kwargs)
            if event.name in ALLOWED_SSE_EVENTS:
                for observer in self.observers:
                    await observer.put(event)

        return wrapper

    async def add_observer(self, observer: "Observer") -> None:
        # Care about disconnected observers
        await self.ensure_observers()
        self.observers.append(observer)

    async def remove_observer(self, observer: "Observer") -> None:
        self.observers.remove(observer)


sse_publisher = Publisher()


class Observer(asyncio.Queue):

    def __init__(self, request, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.request: Request = request

    async def subscribe(self, publisher: Publisher) -> None:
        await publisher.add_observer(self)

    async def unsubscribe(self, publisher: Publisher) -> None:
        await publisher.remove_observer(self)


async def event_generator(observer: Observer):
    WATCHING_DELAY = 0.5  # second

    while True:
        event = await observer.get()
        if event is not None:
            yield event
        await asyncio.sleep(WATCHING_DELAY)


@stream_router.get('/stream')
async def stream(request: Request):
    observer = Observer(request)
    await observer.subscribe(sse_publisher)
    return EventSourceResponse(
        event_generator(observer)
    )
