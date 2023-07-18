from pydantic import BaseModel
from sqlalchemy import Column, String, Enum, DateTime, ForeignKey, Numeric
from sqlalchemy.orm import relationship

from core.database import Model
from manager.fields import ChargePointStatus
from manager.models.location import Location


class ChargePoint(Model):
    __tablename__ = "charge_points"

    id = Column(String, primary_key=True, nullable=False)
    description = Column(String(48), nullable=True)
    status = Column(Enum(ChargePointStatus), default=ChargePointStatus.OFFLINE, index=True)
    last_heartbeat = Column(DateTime, nullable=True)
    manufacturer = Column(String, nullable=True)
    latitude = Column(Numeric, nullable=True)
    longitude = Column(Numeric, nullable=False)
    serial_number = Column(String, nullable=False, unique=True)
    comment = Column(String, nullable=True)
    model = Column(String, nullable=False)
    password = Column(String, nullable=False)

    location_id = Column(String, ForeignKey("locations.id", ondelete="CASCADE"), nullable=False)
    location = relationship(Location, back_populates="charge_points")


class AuthData(BaseModel):
    password: str
