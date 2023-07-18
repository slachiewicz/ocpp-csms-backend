from typing import Type

from httpx import AsyncClient
from pydantic import BaseModel


class ApiClient:

    def __init__(self, host: str, port: int, client: Type[AsyncClient] = AsyncClient):
        self._host = host
        self._port = port
        self._client = client

    @property
    def host(self) -> str:
        return self._host

    @property
    def port(self) -> int:
        return self._port

    def get_uri(self, endpoint: str) -> str:
        host = self.host.rstrip("/")
        endpoint = endpoint.lstrip('/')
        return f"{host}:{self.port}/{endpoint}"

    async def post(self, endpoint: str, data: BaseModel):
        uri = self.get_uri(endpoint)
        async with self._client() as client:
            return await client.post(uri, data=data.json())
