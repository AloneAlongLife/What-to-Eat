from pydantic import Field

from typing import Optional

from .base import Base

class UserBase(Base):
    username: str
    displayname: str
    avatar: bool

class UserUpdate(UserBase):
    displayname: Optional[str] = None
    avatar: Optional[bool] = None
    password: Optional[str] = Field(min_length=8)

class UserCreate(UserBase):
    password: str

class User(UserBase):
    id: int
    uuid: str
