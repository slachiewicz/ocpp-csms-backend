from __future__ import annotations

from functools import wraps
from typing import List, Callable

from core import settings
from sse import observer as obs


class Publisher:
    observers: List[obs.Observer] = []

    async def ensure_observers(self):
        for observer in self.observers:
            if await observer.request.is_disconnected():
                self.observers.remove(observer)
                del observer

    def publish(self, func) -> Callable:
        @wraps(func)
        async def wrapper(*args, **kwargs):
            event = await func(*args, **kwargs)
            if event.name in settings.ALLOWED_SSE_EVENTS:
                for observer in self.observers:
                    await observer.put(event)

        return wrapper

    async def add_observer(self, observer: obs.Observer) -> None:
        # Care about disconnected observers
        await self.ensure_observers()
        self.observers.append(observer)

    async def remove_observer(self, observer: obs.Observer) -> None:
        self.observers.remove(observer)
