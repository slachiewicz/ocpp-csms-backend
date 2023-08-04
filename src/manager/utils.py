import os

from core.settings import LOCK_FOLDER
from manager.exceptions import Forbidden


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
