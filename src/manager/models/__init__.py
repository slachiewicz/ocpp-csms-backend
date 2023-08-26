from __future__ import annotations

from pydantic import BaseModel
from sqlalchemy import Column, String, ForeignKey, Enum, Numeric
from sqlalchemy.orm import relationship

from core.database import Model
from core.fields import ChargePointStatus


class Account(Model):
    __tablename__ = "accounts"

    name = Column(String(48), nullable=False, unique=True)
    locations = relationship("Location",
                             back_populates="account",
                             lazy="joined")

    def __repr__(self) -> str:
        return f"Account: {self.name}, {self.id}"


class Location(Model):
    __tablename__ = "locations"

    name = Column(String(48), nullable=False, unique=True)
    city = Column(String(48), nullable=False)
    address1 = Column(String(48), nullable=False)
    address2 = Column(String(100), nullable=True)
    comment = Column(String(200), nullable=True)

    charge_points = relationship("ChargePoint",
                                 back_populates="location",
                                 lazy="joined")
    account_id = Column(String, ForeignKey("accounts.id", ondelete="CASCADE"), nullable=False)
    account = relationship("Account", back_populates="locations", lazy='joined')

    def __repr__(self) -> str:
        return f"Location: {self.name}, {self.city}, {self.id}"


class ChargePoint(Model):
    __tablename__ = "charge_points"

    id = Column(String, primary_key=True, nullable=False)
    description = Column(String(48), nullable=True)
    status = Column(Enum(ChargePointStatus), default=ChargePointStatus.OFFLINE, index=True)
    manufacturer = Column(String, nullable=True)
    latitude = Column(Numeric, nullable=True)
    longitude = Column(Numeric, nullable=False)
    serial_number = Column(String, nullable=False, unique=True)
    comment = Column(String, nullable=True)
    model = Column(String, nullable=False)
    password = Column(String, nullable=False)

    location_id = Column(String, ForeignKey("locations.id", ondelete="CASCADE"), nullable=False)
    location = relationship("Location", back_populates="charge_points", lazy='joined')

    def __repr__(self):
        return f"ChargePoint (id={self.id}, status={self.status}, location={self.location})"


class AuthData(BaseModel):
    password: str
