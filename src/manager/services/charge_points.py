from loguru import logger
from sqlalchemy import select, update

from core.database import get_session
from manager.models.charge_point import ChargePoint
from manager.views.charge_points import ChargePointCommonView


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


async def get_charge_point(charge_point_id) -> ChargePoint | None:
    async with get_session() as session:
        result = await session.execute(select(ChargePoint).where(ChargePoint.id == charge_point_id))
        return result.scalars().first()
