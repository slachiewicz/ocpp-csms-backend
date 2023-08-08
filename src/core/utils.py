import arrow

from core.settings import UTC_DATETIME_FORMAT


def get_utc_as_string() -> str:
    return arrow.utcnow().datetime.strftime(UTC_DATETIME_FORMAT)
