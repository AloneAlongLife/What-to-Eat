from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from datetime import datetime
from hashlib import sha1
from time import time
from typing import Any, Optional, Union

from models import UserModel
from schemas import User, UserCreate, UserUpdate
from swap import CHANGE_PASSWORD_USER
from utils import password_hash

from .base import CRUDBase

class CRUDUser(CRUDBase[UserModel, User, UserCreate, UserUpdate]):
    def __init__(self) -> None:
        super().__init__(UserModel)
    
    async def get_by_uuid(self, db: AsyncSession, uuid: str) -> Optional[UserModel]:
        query_stat = select(UserModel).where(self.model.uuid == uuid)
        result = await db.execute(query_stat)
        result = result.first()
        
        return result[0] if result else None
    
    async def get_by_username(self, db: AsyncSession, username: str) -> Optional[UserModel]:
        query_stat = select(UserModel).where(self.model.username == username)
        result = await db.execute(query_stat)
        result = result.first()
        
        return result[0] if result else None
    
    async def create(
        self,
        db: AsyncSession,
        obj: UserCreate
    ) -> UserModel:
        dump_data = obj.model_dump(exclude=("password",))
        dump_data["hashpassword"] = password_hash(obj.password)

        new_obj = UserModel(**dump_data)

        uuid = sha1(f"{obj.username}{time()}".encode()).hexdigest()
        if ord(uuid[0]) < 58:
            uuid = chr(ord(uuid[0]) + 49) + uuid[1:]
        new_obj.uuid = uuid

        return self._create(db, new_obj)

    async def update(
        self,
        db: AsyncSession,
        obj: UserModel,
        obj_update: Union[UserUpdate, dict[str, Any], UserModel]
    ) -> UserModel:
        if isinstance(obj_update, dict):
            update_data = obj_update
            if update_data.get("password"):
                update_data["hashpassword"] = password_hash(update_data["password"])
                del update_data["password"]
        else:
            update_data = obj_update.model_dump(
                exclude_unset=True,
                exclude=("password",)
            )
            if obj_update.password:
                update_data["hashpassword"] = password_hash(obj_update.password)
        if update_data.get("hashpassword"):
            CHANGE_PASSWORD_USER[obj.username] = datetime.utcnow().timestamp()
        return await super().update(db, obj, update_data)
