from sqlalchemy import Column, ForeignKey, Integer

from database.database import Base

class ArticleTagsRelationship(Base):
    __tablename__ = "article_tags_rel"

    article_id = Column(Integer, ForeignKey("articles.id"))
    tag_id = Column(Integer, ForeignKey("style_tags.id"))
