from fastapi.encoders import jsonable_encoder
from sqlalchemy import select, Select
from sqlalchemy.exc import IntegrityError
from sqlalchemy.ext.asyncio import AsyncSession

from typing import Any, Generic, Iterator, Optional, Type, TypeVar, Union

from database.database import Base, async_session
from schemas.base import Base as PydanticBase

ModelType = TypeVar("ModelType", bound=Base)
CreateSchemaType = TypeVar("CreateSchemaType", bound=PydanticBase)
UpdateSchemaType = TypeVar("UpdateSchemaType", bound=PydanticBase)
SchemaType = TypeVar("SchemaType", bound=PydanticBase)

# _TSelectParam = TypeVar("_TSelectParam")

class CRUDBase(Generic[ModelType, SchemaType, CreateSchemaType, UpdateSchemaType]):
    def __init__(self, model: Type[ModelType]) -> None:
        self.model = model

    async def get(self, db: AsyncSession, id: int) -> Optional[ModelType]:
        query_stat = select(self.model).where(self.model.id == id)
        result = await db.execute(query_stat)
        result = result.first()
        
        return result[0] if result else None

    async def get_by_ids(self, db: AsyncSession, ids: Iterator[int]) -> Optional[list[ModelType]]:
        query_stat = select(self.model).where(self.model.id.in_(ids))
        result = await db.execute(query_stat)

        return list(map(lambda x: x[0], result.all()))
    
    async def get_all(self, db: AsyncSession) -> Optional[list[ModelType]]:
        query_stat = select(self.model)
        result = await db.execute(query_stat)

        return list(map(lambda x: x[0], result.all()))

    async def get_range(
        self,
        db: AsyncSession,
        statement: Optional[Select] = None,
        start: Optional[int] = None,
        length: Optional[int] = None
    ) -> Optional[list[ModelType]]:
        query_stat = statement if statement else select(self.model)
        query_stat = query_stat.offset(start) if start else query_stat
        query_stat = query_stat.limit(length) if length else query_stat

        result = await db.execute(query_stat)
        
        return list(map(lambda x: x[0], result.all()))

    async def create(
        self,
        db: AsyncSession,
        obj: CreateSchemaType,
    ) -> ModelType:
        obj = self.model(**obj.model_dump())

        return self._create(db, obj)

    async def _create(
        self,
        db: AsyncSession,
        obj: ModelType
    ) -> ModelType:
        try:
            db.add(obj)
            await db.commit()
        except IntegrityError:
            await db.rollback()
        await db.refresh(obj)
        return obj

    async def update(
        self,
        db: AsyncSession,
        obj: ModelType,
        obj_update: Union[UpdateSchemaType, dict[str, Any], ModelType],
    ) -> ModelType:
        if isinstance(obj_update, dict):
            update_data = obj_update
        else:
            update_data = obj_update.model_dump(
                exclude_unset=True
            )
        for field in obj.__dict__:
            if field in update_data:
                setattr(obj, field, update_data[field])

        db.add(obj)
        await db.commit()
        await db.refresh(obj)
        return obj

    async def delete(
        self,
        db: AsyncSession,
        id: int,
    ) -> ModelType:
        obj = await self.get(db, id)

        await db.delete(obj)
        await db.commit()

        return obj
