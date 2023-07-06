from __future__ import annotations

import asyncio
from typing import Dict

from starlette.requests import Request

from sse import publisher as pub

counter = []


class Observer(asyncio.Queue):
    # in order to prevent memory overflow
    max_events_count = 10

    def __init__(self, request, *args, **kwargs):
        super().__init__(*args, **kwargs, maxsize=self.max_events_count)
        self.request: Request = request

    async def subscribe(self, publisher: pub.Publisher) -> None:
        await publisher.add_observer(self)

    async def unsubscribe(self, publisher: pub.Publisher) -> None:
        await publisher.remove_observer(self)

    async def gain_event(self, event: Dict) -> None:
        await self.put(event)

    async def consume_event(self) -> Dict:
        return await self.get()
