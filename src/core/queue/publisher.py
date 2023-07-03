import aio_pika

from core.queue import get_connection, get_channel


async def publish(data: str, to: str) -> None:
    connection = await get_connection()
    channel = await get_channel(connection, to)

    await channel.default_exchange.publish(
        aio_pika.Message(
            bytes(data, "utf-8"),
            content_type="json",
        ),
        routing_key=to,
    )
