import asyncio
from traceback import format_exc

import websockets
from loguru import logger
from ocpp.exceptions import NotSupportedError, FormatViolationError, ProtocolError, \
    PropertyConstraintViolationError
from ocpp.messages import unpack

from charge_point_node.models.on_connection import OnConnectionEvent, LostConnectionEvent
from charge_point_node.protocols import OCPPWebSocketServerProtocol
from charge_point_node.router import Router
from charge_point_node.services.tasks import process_task
from core.queue.consumer import start_consume
from core.queue.publisher import publish
from core.settings import WS_SERVER_PORT, TASKS_QUEUE_NAME

background_tasks = set()
router = Router()


async def watch(connection: OCPPWebSocketServerProtocol):
    while True:

        try:
            raw_msg = await connection.recv()
        except Exception:
            break

        try:
            msg = unpack(raw_msg)
        except (FormatViolationError, ProtocolError, PropertyConstraintViolationError) as exc:
            logger.error("Could not parse message (message=%r, details=%r)" % (raw_msg, format_exc()))
            await connection.send({"code": "validation_failed", "details": exc.description})
            continue
        try:
            await router.handle_on(connection, msg)
        except NotSupportedError:
            logger.error("Caught error during call handling (details=%r)" % format_exc())
            continue
        except Exception as error:
            logger.error("Caught error during call handling (details=%r)" % format_exc())
            response = msg.create_call_error(error).to_json()
            await connection.send(response)


async def on_connect(connection: OCPPWebSocketServerProtocol, path: str):
    charge_point_id = connection.charge_point_id
    logger.info(f"New charge point connected (charge_point_id={charge_point_id})")
    event = OnConnectionEvent(charge_point_id=charge_point_id)
    await publish(event.json(), to=event.target_queue, priority=event.priority)

    await watch(connection)

    logger.info(f"Closed connection (charge_point_id={charge_point_id})")
    event = LostConnectionEvent(charge_point_id=charge_point_id)
    await publish(event.json(), to=event.target_queue, priority=event.priority)


async def main():
    server = await websockets.serve(
        on_connect,
        '0.0.0.0',
        WS_SERVER_PORT,
        create_protocol=OCPPWebSocketServerProtocol
    )
    # Save a reference to the result of this function, to avoid a task disappearing mid-execution.
    # The event loop only keeps weak references to tasks.
    task = asyncio.create_task(
        start_consume(
            TASKS_QUEUE_NAME,
            on_message=lambda data: process_task(data, server))
    )
    background_tasks.add(task)

    await server.wait_closed()


if __name__ == '__main__':
    asyncio.run(main())
