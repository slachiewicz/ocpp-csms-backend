import asyncio
import json
from typing import Dict

from aio_pika.abc import AbstractIncomingMessage

from core.queue import get_connection, get_channel


async def start_consume(
        queue_name,
        on_message,
        prefetch_count=100,  # Maximum message count which will be processing at the same time.
        durable=True
) -> None:
    connection = await get_connection()
    channel = await get_channel(connection, queue_name)

    await channel.set_qos(prefetch_count=prefetch_count)
    queue = await channel.declare_queue(queue_name, durable=durable)

    async def parse_message(message: AbstractIncomingMessage) -> Dict:
        async with message.process():
            return await on_message(json.loads(message.body.decode()))

    await queue.consume(parse_message)

    try:
        # Wait until terminate
        await asyncio.Future()
    finally:
        await connection.close()
