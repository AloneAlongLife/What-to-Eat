from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from models import ArticleModel, UserModel
from schemas import Article, ArticleCreate, ArticleUpdate, User

from hashlib import sha1
from time import time
from typing import Any, Optional, Union

from .base import CRUDBase
from .style_tag import CRUDStyleTag

crud_style_tag = CRUDStyleTag()

class CRUDArticle(CRUDBase[ArticleModel, Article, ArticleCreate, ArticleUpdate]):
    def __init__(self) -> None:
        super().__init__(ArticleModel)
    
    async def create(
        self,
        db: AsyncSession,
        obj: ArticleCreate,
        author: Union[User, UserModel]
    ) -> ArticleModel:
        dump_data = obj.model_dump(exclude=("style_tag_ids",))

        style_tags = await crud_style_tag.get_by_ids(db, obj.style_tag_ids)
        new_obj = self.model(**dump_data)
        new_obj.style_tags = style_tags
        if type(author) == UserModel:
            new_obj.author = author
        else:
            new_obj.author_id = author.id
        
        uuid = sha1(f"{author.username}{time()}".encode()).hexdigest()
        if ord(uuid[0]) < 58:
            uuid = chr(ord(uuid[0]) + 49) + uuid[1:]
        new_obj.uuid = uuid

        return await super()._create(db, new_obj)

    async def get_by_uuid(
        self,
        db: AsyncSession,
        uuid: str,
    ) -> Optional[ArticleModel]:
        query_stat = select(self.model).where(self.model.uuid == uuid)
        result = await db.execute(query_stat)
        result = result.first()
        
        return result[0] if result else None

    async def update(
        self,
        db: AsyncSession,
        obj: ArticleModel,
        obj_update: Union[ArticleUpdate, dict[str, Any], ArticleModel],
    ) -> ArticleModel:
        if isinstance(obj_update, dict):
            update_data = obj_update
        else:
            update_data = obj_update.model_dump(
                exclude_unset=True
            )
        style_tag_ids = update_data.get("style_tag_ids")
        if style_tag_ids:
            obj.style_tags = await crud_style_tag.get_by_ids(db)
        return await super().update(db, obj, update_data)
    
    async def delete_from_obj(
        self,
        db: AsyncSession,
        obj: ArticleModel,
    ) -> ArticleModel:
        obj.style_tags = []
        await db.commit()
        await db.refresh(obj)

        await db.delete(obj)
        await db.commit()

        return obj
