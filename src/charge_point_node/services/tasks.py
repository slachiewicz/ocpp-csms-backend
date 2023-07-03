from aio_pika.abc import AbstractIncomingMessage
from loguru import logger


async def process_tasks(task: AbstractIncomingMessage) -> None:
    task = task.body.decode()
    logger.info(f"Got task from manager (task={task})")
