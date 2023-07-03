import asyncio
import json

import websockets
from loguru import logger
from websockets.legacy.server import WebSocketServerProtocol

from charge_point_node.services.tasks import process_tasks
from core.queue.consumer import start_consume
from core.queue.publisher import publish
from core.settings import WS_SERVER_PORT, TASKS_QUEUE_NAME, EVENTS_QUEUE_NAME


async def on_connect(connection: WebSocketServerProtocol, path: str):
    charge_point_id = path.strip("/")
    logger.info(f"New charge point connected (path={path}, charge_point_id={charge_point_id})")
    event = json.dumps({"event": "new_connection", "charge_point_id": charge_point_id})
    await publish(event, to=EVENTS_QUEUE_NAME)


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
