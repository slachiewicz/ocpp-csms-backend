from __future__ import annotations

from functools import wraps
from typing import Callable

from loguru import logger
from websockets.legacy.server import WebSocketServer

from manager.models import BaseTask


def prepare_task(func) -> Callable:
    @wraps(func)
    async def wrapper(data, *args, **kwargs):
        task = {

        }[data["name"]](**data)
        return await func(task, *args, **kwargs)

    return wrapper


@prepare_task
async def process_task(task: BaseTask, server: WebSocketServer) -> None:
    logger.info(f"Got task from manager (task={task})")
