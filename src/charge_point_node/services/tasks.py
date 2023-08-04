from __future__ import annotations

from functools import wraps
from typing import Callable

from loguru import logger
from websockets.legacy.server import WebSocketServer

from manager.fields import TaskName
from manager.models.tasks.base import BaseTask
from manager.models.tasks.connections import DisconnectTask


def prepare_task(func) -> Callable:
    @wraps(func)
    async def wrapper(data, *args, **kwargs):
        task = {
            TaskName.DISCONNECT: DisconnectTask
        }[data["name"]](**data)
        return await func(task, *args, **kwargs)

    return wrapper


@prepare_task
async def process_task(task: BaseTask, server: WebSocketServer) -> None:
    logger.info(f"Got task from manager (task={task})")
    connections = [conn for conn in server.websockets if conn.charge_point_id == task.charge_point_id]
    if not connections:
        return
    connection = connections[0]
    if task.name is TaskName.DISCONNECT:
        await connection.close()
