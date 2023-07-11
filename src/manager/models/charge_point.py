from sqlalchemy import Column, String, Enum, DateTime, ForeignKey
from sqlalchemy.orm import relationship

from core.database import Model
from manager.fields import ChargePointStatus


class ChargePoint(Model):
    __tablename__ = "charge_points"

    id = Column(String, primary_key=True, nullable=False)
    description = Column(String(48), nullable=True)
    status = Column(Enum(ChargePointStatus), default=ChargePointStatus.OFFLINE, index=True)
    last_heartbeat = Column(DateTime, nullable=True)

    location_id = Column(String, ForeignKey("locations.id", ondelete="CASCADE"), nullable=False)
    location = relationship("Location", back_populates="charge_points")
