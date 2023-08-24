import asyncio
from typing import Tuple

from fastapi import APIRouter, HTTPException, status, Depends
from sqlalchemy import select

from core.queue.publisher import publish
from manager.auth.charge_points import is_relevant_password
from manager.models import AuthData, Account, Location, ChargePoint
from manager.models.tasks.connections import DisconnectTask
from manager.services.accounts import get_account
from manager.services.charge_points import (
    get_charge_point,
    get_statuses_counts
)
from manager.utils import acquire_lock, params_extractor, paginate
from manager.views.charge_points import StatusCount, PaginatedChargePointsView

charge_points_router = APIRouter(
    prefix="/{account_id}/charge_points",
    tags=["charge_points"]
)


@charge_points_router.post(
    "/{charge_point_id}",
    status_code=status.HTTP_200_OK
)
async def authenticate(charge_point_id: str, data: AuthData):
    charge_point = await get_charge_point(charge_point_id)
    if not charge_point \
            or not await is_relevant_password(
        data.password,
        charge_point.password
    ):
        raise HTTPException(status.HTTP_401_UNAUTHORIZED)


@charge_points_router.get("/", status_code=status.HTTP_200_OK)
async def list_charge_points(
        account: Account = Depends(get_account),
        params: Tuple = Depends(params_extractor)
) -> PaginatedChargePointsView:
    criterias = [
        Location.account_id == account.id,
        Location.is_active.is_(True),
        ChargePoint.is_active.is_(True)
    ]
    query = select(ChargePoint).join(Location)
    for criteria in criterias:
        query = query.where(criteria)
    items, pagination = await paginate(ChargePoint, query, *params)
    await asyncio.sleep(2)
    return PaginatedChargePointsView(items=items, pagination=pagination)


@charge_points_router.get(
    "/counters",
    status_code=status.HTTP_200_OK,
    response_model=StatusCount
)
async def get_counters():
    return await get_statuses_counts()


@charge_points_router.patch(
    "/{charge_point_id}",
    status_code=status.HTTP_204_NO_CONTENT
)
async def disconnect(charge_point_id: str):
    await acquire_lock(charge_point_id)
    task = DisconnectTask(charge_point_id=charge_point_id)
    await publish(task.json(), to=task.target_queue)
