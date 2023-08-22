from __future__ import annotations

from typing import List

from pydantic import BaseModel, validator

from manager.models import Location
from manager.views import PaginationView


class SimpleLocation(BaseModel):
    name: str
    city: str
    address1: str

    class Config:
        orm_mode = True


class PaginatedLocationsView(BaseModel):
    items: List[SimpleLocation]
    pagination: PaginationView


class CreateLocationView(BaseModel):
    name: str
    city: str
    address1: str

    @validator("name")
    def validate_name_length(cls, value):
        length = Location.name.property.columns[0].type.length
        if len(value) > length:
            raise ValueError(f"Too long 'name' value ({length} maximum.)")
        return value

    @validator("city")
    def validate_city_length(cls, value):
        length = Location.city.property.columns[0].type.length
        if len(value) > length:
            raise ValueError(f"Too long 'city' value ({length} maximum.)")
        return value

    @validator("address1")
    def validate_address1_length(cls, value):
        length = Location.address1.property.columns[0].type.length
        if len(value) > length:
            raise ValueError(f"Too long 'address1' value ({length} maximum.)")
        return value
