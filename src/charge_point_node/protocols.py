import base64
import re
from http import HTTPStatus
from traceback import format_exc

from loguru import logger
from websockets.datastructures import Headers
from websockets.exceptions import InvalidHandshake
from websockets.legacy.server import WebSocketServerProtocol

from charge_point_node.views import ChargePointAuthView
from core.http import ApiClient
from core.settings import HTTP_SERVER_HOST, HTTP_SERVER_PORT

api_client = ApiClient(host=HTTP_SERVER_HOST, port=HTTP_SERVER_PORT)


class OCPPWebSocketServerProtocol(WebSocketServerProtocol):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.logger = logger

    async def extract_charge_point_id(self, path: str) -> str:
        return path.split("/")[-1].strip("/")

    async def _extract_password(self, charge_point_id: str, headers: Headers) -> str | None:
        logger.info(f"Start validation (charge_point_id={charge_point_id})")
        authorization_data = headers.get("Authorization")

        if not authorization_data:
            logger.info(f"Could not get Authorization header (charge_point_id={charge_point_id})")
            return

        basic_search = re.compile(r"Basic (.+)").search(authorization_data)
        if basic_search is None:
            logger.info(f"Could get recognize auth scheme (charge_point_id={charge_point_id})")
            return

        try:
            basic_search_result = base64.b64decode(basic_search.group(1).encode()).decode()
        except Exception:
            logger.error("Count not decode token (charge_point_id=%s, error=%r)"
                         % (charge_point_id, format_exc()))
            return

        credentials_search = re.compile(f"(.+)[:/\\|]]*(.+)").search(basic_search_result)
        if credentials_search is None:
            logger.info(f"Could not parse credentials (charge_point_id={charge_point_id})")
            return

        username = credentials_search.group(1)
        password = credentials_search.group(2)
        # The username SHALL be equal to the Charging Station identity
        if charge_point_id != username:
            logger.info(
                f"Charge point id and username do not match "
                f"(username={username}, charge_point_id={charge_point_id})")
            return None

        return password

    async def process_request(self, path, headers: Headers):
        """
        An implementation of the OCPP Security profile (Basic HTTP Auth)
        :param path:
        :param headers:
        :return:
        """
        charge_point_id = await self.extract_charge_point_id(path)
        password = await self._extract_password(charge_point_id, headers)

        if not password:
            response_status = HTTPStatus.UNAUTHORIZED
        else:
            response = await api_client.post(
                f"charge_points/{charge_point_id}",
                data=ChargePointAuthView(password=password)
            )
            response_status = HTTPStatus(response.status_code)

        if not response_status is HTTPStatus.OK:
            self.write_http_response(response_status, Headers())
            raise InvalidHandshake
