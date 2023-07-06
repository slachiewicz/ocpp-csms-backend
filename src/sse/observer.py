from __future__ import annotations

import asyncio

from starlette.requests import Request

from sse import publisher as pub


class Observer(asyncio.Queue):

    def __init__(self, request, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.request: Request = request

    async def subscribe(self, publisher: pub.Publisher) -> None:
        await publisher.add_observer(self)

    async def unsubscribe(self, publisher: pub.Publisher) -> None:
        await publisher.remove_observer(self)
