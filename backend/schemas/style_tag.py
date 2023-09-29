from typing import Optional

from .base import Base

class StyleTagBase(Base):
    tag_name: str

class StyleTagUpdate(StyleTagBase):
    tag_name: Optional[str] = None

class StyleTagCreate(StyleTagBase):
    pass

class StyleTag(StyleTagBase):
    id: int
