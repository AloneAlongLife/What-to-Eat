from sqlalchemy import Column, Float, ForeignKey, Integer, JSON, String
from sqlalchemy.orm import relationship

from datetime import datetime

from database.database import Base

class ArticleModel(Base):
    __tablename__ = "articles"

    uuid = Column(String, unique=True, nullable=False)
    food_score = Column(Integer, nullable=False)
    service_score = Column(Integer, nullable=False)
    environment_score = Column(Integer, nullable=False)
    flavor = Column(String, nullable=False, default="")
    quantity = Column(String, nullable=False, default="")
    speed = Column(String, nullable=False, default="")
    environment = Column(String, nullable=False, default="")
    context = Column(String, nullable=False, default="")
    comment = Column(String, nullable=False)
    create_at = Column(Float, nullable=False, default=datetime.utcnow().timestamp)
    cost = Column(Integer, nullable=False)

    food_pictures = Column(JSON, nullable=False, default=[])
    shop_pictures = Column(JSON, nullable=False, default=[])

    author_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    restaurant_id = Column(Integer, ForeignKey("restaurants.id"), nullable=False)

    author = relationship("UserModel", back_populates="articles", lazy="selectin")
    restaurant = relationship("RestaurantModel", back_populates="articles", lazy="selectin")
    style_tags = relationship("StyleTagModel", secondary="article_tags_rel", back_populates="articles", lazy="selectin")
