from fastapi import APIRouter, status
from sqlalchemy.ext.asyncio import AsyncSession

from typing import Optional

from crud import CRUDUser
from schemas import UserRelation

from ..depends import db_depends

router = APIRouter(
    prefix="/user",
    tags=["user"],
)
crud_user = CRUDUser()

@router.get(
    path="/{user_uuid}",
    response_model=Optional[UserRelation],
    status_code=status.HTTP_200_OK
)
async def get_user_by_uuid(
    user_uuid: str,
    db: AsyncSession = db_depends
):
    result = await crud_user.get_by_uuid(db, user_uuid)

    return result

# Get User By Username
# @router.get(
#     path="/username/{username}",
#     response_model=Optional[UserRelation],
#     status_code=status.HTTP_200_OK
# )
# async def get_user_by_uuid(
#     username: str,
#     db: AsyncSession = db_depends
# ):
#     result = await crud_user.get_by_username(db, username)

#     return result
