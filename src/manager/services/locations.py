from loguru import logger
from sqlalchemy.ext.asyncio import AsyncSession

from manager.models import Location, Account
from manager.views.locations import CreateLocationView


async def create_location(
        account: Account,
        data: CreateLocationView,
        session: AsyncSession
) -> Location:
    logger.info(f"Start creating location (account={account}, data: {data}).")
    location = Location(account_id=account.id, **data.dict())
    session.add(location)
    return location
