from fastapi import APIRouter, HTTPException, status

from manager.auth.charge_points import is_relevant_password
from manager.models.charge_point import AuthData
from manager.services.charge_points import get_charge_point

charge_points_router = APIRouter(
    prefix="/charge_points",
    tags=["charge_points"]
)


@charge_points_router.post(
    "/{charge_point_id}",
    status_code=status.HTTP_200_OK
)
async def authenticate(charge_point_id: str, data: AuthData):
    charge_point = await get_charge_point(charge_point_id)
    if not charge_point or not await is_relevant_password(data.password, charge_point.password):
        raise HTTPException(status.HTTP_401_UNAUTHORIZED)
