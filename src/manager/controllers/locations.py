from typing import Tuple
import asyncio

from fastapi import APIRouter, status, Depends
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from core.database import get_session
from manager.models import Account, Location
from manager.services.accounts import get_account
from manager.services.locations import create_location
from manager.utils import params_extractor, paginate
from manager.views.locations import (
    SimpleLocation,
    CreateLocationView, PaginatedLocationsView
)

locations_router = APIRouter(
    prefix="/{account_id}/locations",
    tags=["locations"]
)


@locations_router.get("/", status_code=status.HTTP_200_OK)
async def list_locations(
        account: Account = Depends(get_account),
        params: Tuple = Depends(params_extractor)
):
    criterias = [
        Location.account_id == account.id,
        Location.is_active.is_(True)
    ]
    query = select(Location)
    for criteria in criterias:
        query = query.where(criteria)
    items, pagination = await paginate(Location, query, *params)
    await asyncio.sleep(2)
    return PaginatedLocationsView(items=items, pagination=pagination)


@locations_router.post(
    "/",
    status_code=status.HTTP_201_CREATED,
    response_model=SimpleLocation
)
async def add_location(
        data: CreateLocationView,
        account: Account = Depends(get_account),
        session: AsyncSession = Depends(get_session)
):
    location = await create_location(account, data, session)
    await session.commit()
    return location
