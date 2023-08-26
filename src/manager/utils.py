import os
from typing import Tuple, List

import math
from fastapi import Query
from sqlalchemy import Select, select, func

from core.database import Model, get_contextual_session
from core.settings import LOCK_FOLDER
from manager.exceptions import Forbidden
from manager.views import PaginationView


def _slugify(value: str) -> str:
    return "".join([i for i in value if i.isalpha() or i.isdigit()])


async def acquire_lock(charge_point_id: str) -> None:
    path = os.path.join(LOCK_FOLDER, _slugify(charge_point_id))
    if os.path.exists(path):
        raise Forbidden(detail="Somebody has taken the station. Please, try again later.")
    with open(path, "w"):
        pass


async def release_lock(charge_point_id: str) -> None:
    path = os.path.join(LOCK_FOLDER, _slugify(charge_point_id))
    if os.path.exists(path):
        os.remove(path)


def params_extractor(
        page: int = Query(1, ge=1),
        size: int = Query(5, gt=0)
) -> Tuple:
    return page, size


async def paginate(
        model: Model,
        query: Select,
        page: int,
        size: int
) -> Tuple[List, PaginationView]:
    async with get_contextual_session() as session:
        count = await session.execute(select(func.count(model.id)) \
                                      .filter_by(is_active=True))
        query = query.limit(size).offset(size * (page - 1))

        result = await session.execute(query)
        items = result.unique().scalars().fetchall()

        total = count.scalar_one()
        pagination = PaginationView(
            current_page=page,
            last_page=math.ceil(total / size) or 1,
            total=total
        )

        return items, pagination
