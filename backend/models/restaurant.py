from sqlalchemy import Column, Integer, JSON, String
from sqlalchemy.orm import relationship

from database.database import Base

class RestaurantModel(Base):
    __tablename__ = "restaurants"

    uuid = Column(String, unique=True, nullable=False)
    name = Column(String, nullable=False)
    location = Column(String, nullable=False)
    location_tag = Column(String, nullable=False)
    type_tag = Column(String, nullable=False)
    city = Column(String, nullable=False)
    map_embed = Column(String, nullable=False, default="")
    contact = Column(String, nullable=False, default="")
    website = Column(String, nullable=False, default="")
    business_hours = Column(JSON, nullable=False)

    data_creator_id = Column(Integer, nullable=True)
    data_editor_ids = Column(JSON, nullable=False, default=[])
    articles = relationship("ArticleModel", back_populates="restaurant", lazy="selectin")
