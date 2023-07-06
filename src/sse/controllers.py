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
    observers: List[asyncio.Queue] = []

    def publish(self, func) -> Callable:
        @wraps(func)
        async def wrapper(*args, **kwargs):
            event = await func(*args, **kwargs)
            if event.name in ALLOWED_SSE_EVENTS:
                for observer in self.observers:
                    await observer.put(event)

        return wrapper

    async def add_observer(self, observer: asyncio.Queue) -> None:
        self.observers.append(observer)

    async def remove_observer(self, observer: asyncio.Queue) -> None:
        self.observers.remove(observer)


sse_publisher = Publisher()


class Observer(asyncio.Queue):

    async def subscribe(self, publisher: Publisher) -> None:
        await publisher.add_observer(self)

    async def unsubscribe(self, publisher: Publisher) -> None:
        await publisher.remove_observer(self)


async def event_generator(request: Request, observer: Observer, sse_publisher: Publisher):
    WATCHING_DELAY = 0.5  # second

    while True:
        if await request.is_disconnected():
            await observer.unsubscribe(sse_publisher)
            del observer

        event = await observer.get()
        if event:
            yield event
        await asyncio.sleep(WATCHING_DELAY)


@stream_router.get('/stream')
async def stream(request: Request):
    observer = Observer()
    await observer.subscribe(sse_publisher)
    return EventSourceResponse(
        event_generator(request, observer, sse_publisher)
    )
