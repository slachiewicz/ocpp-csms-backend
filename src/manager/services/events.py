from aio_pika.abc import AbstractIncomingMessage
from loguru import logger


async def process_event(event: AbstractIncomingMessage) -> None:
    async with event.process():
        event = event.body.decode()
        logger.info(f"Got event from charge point node (event={event})")
