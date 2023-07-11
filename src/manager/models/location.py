from sqlalchemy import Column, String
from sqlalchemy.orm import relationship

from core.database import Model


class Location(Model):
    __tablename__ = "locations"

    name = Column(String(48), nullable=False)
    city = Column(String(48), nullable=False)
    address1 = Column(String(48), nullable=False)
    address2 = Column(String(100), nullable=True)
    comment = Column(String(200), nullable=True)

    charge_points = relationship("ChargePoint",
                                 back_populates="location",
                                 lazy="joined")
