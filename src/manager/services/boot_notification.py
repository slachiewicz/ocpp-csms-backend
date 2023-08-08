from ocpp.v201.enums import RegistrationStatusType

from charge_point_node.models.base import BaseEvent
from core.utils import get_utc_as_string
from manager.models.tasks.boot_notification import BootNotificationTask


async def process_boot_notification(event: BaseEvent) -> BootNotificationTask:
    # Do some logic here

    return BootNotificationTask(
        message_id=event.message_id,
        charge_point_id=event.charge_point_id,
        current_time=get_utc_as_string(),
        interval=20,
        status=RegistrationStatusType.accepted
    )
