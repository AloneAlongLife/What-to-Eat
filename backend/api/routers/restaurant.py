from sqlalchemy.ext.asyncio import AsyncSession
from fastapi import APIRouter, status
from fastapi.exceptions import HTTPException

from crud import CRUDRestaurant
from models import UserModel
from schemas import RestaurantCreate, RestaurantUpdate, RestaurantRelation

from typing import List, Optional

from ..depends import db_depends, user_depends

router = APIRouter(
    prefix="/restaurant",
    tags=["Restaurant"],
)
crud_restaurant = CRUDRestaurant()
not_found = HTTPException(
    status_code=status.HTTP_404_NOT_FOUND,
    detail="Restaurant not found."
)

@router.get(
    path="/",
    response_model=List[RestaurantRelation],
    status_code=status.HTTP_200_OK,
)
async def get_all_restaurant(
    db: AsyncSession = db_depends,
    page: Optional[int] = None,
    num_per_page: Optional[int] = None,
):
    page = -1 if page is None else page
    num_per_page = -1 if num_per_page is None else num_per_page

    if page < 0 or num_per_page <= 0:
        result = await crud_restaurant.get_all(db)
    else:
        result = await crud_restaurant.get_range(
            db,
            start=page * num_per_page,
            length=num_per_page,
        )
    return result

@router.get(
    path="/{restaurant_uuid}",
    response_model=List[RestaurantRelation],
    status_code=status.HTTP_200_OK,
)
async def get_restaurant_by_uuid(
    restaurant_uuid: str,
    db: AsyncSession = db_depends,
):
    result = await crud_restaurant.get_by_uuid(db, restaurant_uuid)
    if result is None:
        raise not_found
    return result

@router.post(
    path="/",
    response_model=RestaurantRelation,
    status_code=status.HTTP_201_CREATED,
)
async def new_restaurant(
    article: RestaurantCreate,
    db: AsyncSession = db_depends,
    user: UserModel = user_depends,
):
    result = await crud_restaurant.create(db, article, user)
    print(result.__dict__)
    return result


@router.put(
    path="/{restaurant_uuid}",
    response_model=RestaurantRelation,
    status_code=status.HTTP_200_OK,
)
async def update_restaurant(
    restaurant_uuid: str,
    restaurant_update: RestaurantUpdate,
    db: AsyncSession = db_depends,
    user: UserModel = user_depends,
):
    restaurant = await crud_restaurant.get_by_uuid(db, restaurant_uuid)
    if restaurant is None:
        raise not_found
    restaurant = await crud_restaurant.update(
        db,
        restaurant,
        restaurant_update,
        user.id
    )
    return restaurant

