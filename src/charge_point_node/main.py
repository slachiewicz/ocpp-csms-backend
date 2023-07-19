import asyncio

import websockets
from loguru import logger

from charge_point_node.models.on_connection import OnConnectionEvent, LostConnectionEvent
from charge_point_node.protocols import OCPPWebSocketServerProtocol
from charge_point_node.services.tasks import process_task
from core.queue.consumer import start_consume
from core.queue.publisher import publish
from core.settings import WS_SERVER_PORT, TASKS_QUEUE_NAME


async def on_connect(connection: OCPPWebSocketServerProtocol, path: str):
    charge_point_id = await connection.extract_charge_point_id(path)
    logger.info(
        f"New charge point connected "
        f"(charge_point_id={charge_point_id})"
    )
    event = OnConnectionEvent(
        charge_point_id=charge_point_id
    )
    await publish(event.json(), to=event.target_queue)

    while True:
        if connection.closed:
            break
        await asyncio.sleep(3)

    logger.info(
        f"Closed connection (charge_point_id={charge_point_id})")
    event = LostConnectionEvent(
        charge_point_id=charge_point_id
    )
    await publish(event.json(), to=event.target_queue)

    raise asyncio.CancelledError


async def main():
    server = await websockets.serve(
        on_connect,
        '0.0.0.0',
        WS_SERVER_PORT,
        create_protocol=OCPPWebSocketServerProtocol
    )
    asyncio.ensure_future(
        start_consume(
            TASKS_QUEUE_NAME,
            on_message=lambda data: process_task(data, server))
    )
    await server.wait_closed()


if __name__ == '__main__':
    asyncio.run(main())
