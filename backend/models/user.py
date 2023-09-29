from sqlalchemy import Boolean, Column, String
from sqlalchemy.orm import relationship

from database.database import Base

class UserModel(Base):
    __tablename__ = "users"

    uuid = Column(String, unique=True, nullable=False)
    username = Column(String, unique=True, nullable=False)
    displayname = Column(String, unique=True, nullable=False)
    hashpassword = Column(String, nullable=False)
    avatar = Column(Boolean, default=False)
    disable = Column(Boolean, default=False)

    articles = relationship("ArticleModel", back_populates="author", lazy="selectin")
