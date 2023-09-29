from pydantic import validator, Field

from xml.etree import ElementTree as ET
from typing import List, Optional

from .base import Base

class BusinessHours(Base):
    rest: bool
    start: int = Field(0, ge=0, lt=1440)
    end: int = Field(0, ge=0, lt=1440)

    @validator("end")
    def valid_end(cls, value: int, values: dict[str]):
        if values["rest"]:
            return value
        assert value >= values["start"]
        return value

class RestaurantBase(Base):
    name: str
    location: str
    location_tag: str
    type_tag: str
    city: str
    map_embed: str = ""
    contact: str = ""
    website: str = ""
    business_hours: List[BusinessHours] = Field(min_length=7, max_length=7)

    @validator("map_embed")
    def valid_map_embed(cls, value: str):
        if value.startswith("https://www.google.com/maps/embed"):
            return value
        try:
            return ET.fromstring(value).attrib.get("src", "")
        except:
            return ""

class RestaurantUpdate(RestaurantBase):
    name: Optional[str] = None
    location: Optional[str] = None
    location_tag: Optional[str] = None
    type_tag: Optional[str] = None
    city: Optional[str] = None
    map_embed: Optional[str] = None
    contact: Optional[str] = None
    website: Optional[str] = None
    business_hours: Optional[List[BusinessHours]] = None

class RestaurantCreate(RestaurantBase):
    pass

class Restaurant(RestaurantBase):
    id: int
    uuid: str
