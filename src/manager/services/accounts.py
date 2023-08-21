from fastapi import Depends
from sqlalchemy import select

from core.database import get_session, get_contextual_session
from manager.models import Account
from manager.views.accounts import CreateAccountView


async def get_account(
        account_id: str,
        session=Depends(get_session)
) -> Account:
    result = await session.execute(
        select(Account).where(Account.id == account_id)
    )
    return result.scalars().first()


async def create_account(data: CreateAccountView) -> Account:
    async with get_contextual_session() as session:
        account = Account(**data.dict())
        session.add(account)
        await session.commit()
        return account
