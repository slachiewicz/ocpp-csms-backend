from __future__ import annotations

from functools import wraps
from typing import List, Callable

from charge_point_node.models.base import BaseEvent
from core import settings
from sse import observer as obs
from sse.views import Redactor


class Publisher:
    observers: List[obs.Observer] = []
    redactor: Redactor = Redactor()

    async def notify_observer(self, observer: obs.Observer, event: BaseEvent) -> None:
        await observer.gain_event(
            await self.redactor.prepare_event(event)
        )

    async def ensure_observers(self) -> None:
        """
        Remove inactive observers from the 'observers' list.
        :return:
        """
        for observer in self.observers:
            if await observer.request.is_disconnected():
                self.observers.remove(observer)
                del observer

    def publish(self, func) -> Callable:
        """
        Publish new event for all observers in the list
        :param func:
        :return:
        """

        @wraps(func)
        async def wrapper(*args, **kwargs):
            event = await func(*args, **kwargs)
            if event.name in settings.ALLOWED_SSE_EVENTS:
                for observer in self.observers:
                    await self.notify_observer(observer, event)

        return wrapper

    async def add_observer(self, observer: obs.Observer) -> None:
        await self.ensure_observers()
        self.observers.append(observer)

    async def remove_observer(self, observer: obs.Observer) -> None:
        self.observers.remove(observer)
