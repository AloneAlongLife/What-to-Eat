from sqlalchemy import Column, String
from sqlalchemy.orm import relationship

from database.database import Base

class StyleTagModel(Base):
    __tablename__ = "style_tags"

    tag_name = Column(String, unique=True, nullable=False)
    articles = relationship("ArticleModel", secondary="article_tags_rel", back_populates="style_tags", lazy="selectin")
