import asyncio

import websockets
from loguru import logger
from websockets.legacy.server import WebSocketServerProtocol

from charge_point_node.models.on_connection import OnConnectionEvent
from charge_point_node.services.tasks import process_tasks
from core.queue.consumer import start_consume
from core.queue.publisher import publish
from core.settings import WS_SERVER_PORT, TASKS_QUEUE_NAME


async def on_connect(connection: WebSocketServerProtocol, path: str):
    charge_point_id = path.strip("/")
    logger.info((f"New charge point connected "
                 f"(path={path}, charge_point_id={charge_point_id})"))
    event = OnConnectionEvent(charge_point_id=charge_point_id)
    await publish(event.json(), to=event.target_queue)


async def main():
    asyncio.ensure_future(
        start_consume(TASKS_QUEUE_NAME, on_message=process_tasks)
    )

    server = await websockets.serve(
        on_connect,
        '0.0.0.0',
        WS_SERVER_PORT
    )
    await server.wait_closed()


if __name__ == '__main__':
    asyncio.run(main())
