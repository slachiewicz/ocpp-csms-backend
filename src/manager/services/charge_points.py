import asyncio
from typing import Dict

from loguru import logger
from sqlalchemy import select, update, text

from core.database import get_session
from core.fields import ChargePointStatus
from manager.models import ChargePoint
from manager.views.charge_points import ChargePointCommonView


async def list_charge_points():
    async with get_session() as session:
        result = await session.execute(select(ChargePoint))
        await asyncio.sleep(2)
        return result.scalars().fetchall()


async def get_charge_point(charge_point_id) -> ChargePoint | None:
    async with get_session() as session:
        result = await session.execute(select(ChargePoint).where(ChargePoint.id == charge_point_id))
        return result.scalars().first()


async def update_charge_point(
        charge_point_id: str,
        data: ChargePointCommonView
) -> None:
    logger.info((f"Start process update charge point status "
                 f"(charge_point_id={charge_point_id}, data={data})"))
    async with get_session() as session:
        await session.execute(update(ChargePoint) \
                              .where(ChargePoint.id == charge_point_id) \
                              .values(**data.dict(exclude_unset=True)))
        await session.commit()


async def get_statuses_counts() -> Dict:
    """
    A dict with statuses and counts. Example:
    {'offline': 1, 'available': 0, 'reserved': 0, 'charging': 0}
    """
    query = ""
    mapper = {item.value.upper(): item.value.lower() for item in ChargePointStatus}

    for key in mapper:
        query += f" (SELECT COUNT(id) FROM charge_points WHERE status = '{key}') AS {mapper[key]},"
    query = f"SELECT {query}".rstrip(",") + ";"

    async with get_session() as session:
        result = await session.execute(text(query))
        data = result.fetchone()
        await asyncio.sleep(2)
        return {item: getattr(data, item) for item in mapper.values()}
