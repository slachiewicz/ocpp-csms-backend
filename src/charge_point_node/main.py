import asyncio

import websockets
from loguru import logger

from core import settings


async def on_connect(connection, path):
    logger.info(f"Got connection (path={path}).")
    pass


async def main():
    server = await websockets.serve(
        on_connect,
        '0.0.0.0',
        settings.WS_SERVER_PORT
    )
    await server.wait_closed()

if __name__ == '__main__':
    asyncio.run(main())

