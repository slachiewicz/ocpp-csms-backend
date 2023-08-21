from fastapi import APIRouter, status, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from core.database import get_session
from manager.models import Account
from manager.services.accounts import get_account
from manager.services.locations import create_location
from manager.views.locations import SimpleLocation, CreateLocationView

locations_router = APIRouter(
    prefix="/{account_id}/locations",
    tags=["locations"]
)


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
