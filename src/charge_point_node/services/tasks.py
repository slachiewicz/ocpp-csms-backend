from __future__ import annotations

from functools import wraps
from typing import Callable

from loguru import logger
from ocpp.v201.enums import Action
from websockets.legacy.server import WebSocketServer

from charge_point_node.router import Router
from core.fields import ActionName
from manager.models.tasks.base import BaseTask
from manager.models.tasks.boot_notification import BootNotificationTask
from manager.models.tasks.connections import DisconnectTask
from manager.models.tasks.heartbeat import HeartbeatTask

router = Router()


def prepare_task(func) -> Callable:
    @wraps(func)
    async def wrapper(data, *args, **kwargs):
        task = {
            ActionName.DISCONNECT: DisconnectTask,
            Action.BootNotification: BootNotificationTask,
            Action.Heartbeat: HeartbeatTask
        }[data["action"]](**data)
        return await func(task, *args, **kwargs)

    return wrapper


@prepare_task
async def process_task(task: BaseTask, server: WebSocketServer) -> None:
    logger.info(f"Got task from manager (task={task})")
    connections = [conn for conn in server.websockets if conn.charge_point_id == task.charge_point_id]
    if not connections:
        return
    connection = connections[0]

    if task.action is ActionName.DISCONNECT:
        await connection.close()
        return

    await router.handle_out(connection, task)
