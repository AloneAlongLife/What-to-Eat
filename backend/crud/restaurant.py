from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from hashlib import sha1
from time import time
from typing import Any, Optional, Union

from models import RestaurantModel, UserModel
from schemas import Restaurant, RestaurantCreate, RestaurantUpdate, User

from .base import CRUDBase

class CRUDRestaurant(CRUDBase[RestaurantModel, Restaurant, RestaurantCreate, RestaurantUpdate]):
    def __init__(self) -> None:
        super().__init__(RestaurantModel)

    async def get_by_uuid(
        self,
        db: AsyncSession,
        uuid: str,
    ) -> Optional[RestaurantModel]:
        query_stat = select(self.model).where(self.model.uuid == uuid)
        result = await db.execute(query_stat)
        result = result.first()
        
        return result[0] if result else None
    
    async def create(
        self,
        db: AsyncSession,
        obj: RestaurantCreate,
        author: Union[User, UserModel]
    ) -> RestaurantModel:
        dump_data = obj.model_dump()

        new_obj = self.model(**dump_data)
        new_obj.data_creator_id = author.id
        
        uuid = sha1(f"{author.username}{time()}".encode()).hexdigest()
        if ord(uuid[0]) < 58:
            uuid = chr(ord(uuid[0]) + 49) + uuid[1:]
        new_obj.uuid = uuid

        return await super()._create(db, new_obj)

    async def update(
        self,
        db: AsyncSession,
        obj: RestaurantModel,
        obj_update: Union[RestaurantUpdate, dict[str, Any], RestaurantModel],
        user_id: int,
    ) -> RestaurantModel:
        obj.data_editor_ids.append(user_id)
        return await super().update(db, obj, obj_update)
