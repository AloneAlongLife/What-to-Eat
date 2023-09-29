from pydantic import Field

from typing import List, Optional

from .base import Base

class ArticleBase(Base):
    food_score: int = Field(ge=0, le=10)
    service_score: int = Field(ge=0, le=10)
    environment_score: int = Field(ge=0, le=10)
    flavor: str = ""
    quantity: str = ""
    speed: str = ""
    environment: str = ""
    context: str = ""
    comment: str
    cost: int
    food_pictures: List[str] = []
    shop_pictures: List[str] = []

class ArticleUpdate(ArticleBase):
    food_score: Optional[int] = None
    service_score: Optional[int] = None
    environment_score: Optional[int] = None
    flavor: Optional[str] = None
    quantity: Optional[str] = None
    speed: Optional[str] = None
    environment: Optional[str] = None
    context: Optional[str] = None
    comment: Optional[str] = None
    cost: Optional[int] = None
    food_pictures: Optional[List[str]] = None
    shop_pictures: Optional[List[str]] = None
    style_tag_ids: Optional[List[int]] = None

class ArticleCreate(ArticleBase):
    restaurant_id: int
    style_tag_ids: List[int]

class Article(ArticleBase):
    id: int
    uuid: str
    create_at: float
