from sqlalchemy.ext.asyncio import AsyncSession
from fastapi import APIRouter, status
from fastapi.exceptions import HTTPException

from crud import CRUDArticle
from models import UserModel
from schemas import ArticleCreate, ArticleUpdate, ArticleRelation

from typing import List, Optional

from ..depends import db_depends, user_depends

router = APIRouter(
    prefix="/article",
    tags=["Article"],
)
crud_article = CRUDArticle()
permission_denied = HTTPException(
    status_code=status.HTTP_403_FORBIDDEN,
    detail="Permission denied."
)
not_found = HTTPException(
    status_code=status.HTTP_404_NOT_FOUND,
    detail="Article not found."
)

@router.get(
    path="/",
    response_model=List[ArticleRelation],
    status_code=status.HTTP_200_OK,
)
async def get_article(
    db: AsyncSession = db_depends,
    page: Optional[int] = None,
    num_per_page: Optional[int] = None,
):
    page = -1 if page is None else page
    num_per_page = -1 if num_per_page is None else num_per_page

    if page < 0 or num_per_page <= 0:
        result = await crud_article.get_all(db)
    else:
        result = await crud_article.get_range(
            db,
            start=page * num_per_page,
            length=num_per_page,
        )
    return result

@router.get(
    path="/{article_uuid}",
    response_model=ArticleRelation,
    status_code=status.HTTP_200_OK,
)
async def get_article_by_uuid(
    article_uuid: str,
    db: AsyncSession = db_depends,
):
    result = await crud_article.get_by_uuid(db, article_uuid)
    if result is None:
        raise not_found
    return result

@router.post(
    path="/",
    response_model=ArticleRelation,
    status_code=status.HTTP_201_CREATED,
)
async def new_article(
    article: ArticleCreate,
    db: AsyncSession = db_depends,
    user: UserModel = user_depends,
):
    result = await crud_article.create(db, article, user)
    return result

@router.put(
    path="/{article_uuid}",
    response_model=ArticleRelation,
    status_code=status.HTTP_200_OK,
)
async def update_article(
    article_uuid: str,
    article_update: ArticleUpdate,
    db: AsyncSession = db_depends,
    user: UserModel = user_depends,
):
    article = await crud_article.get_by_uuid(db, article_uuid)
    if article is None:
        raise not_found
    if article.author_id != user.id:
        raise permission_denied
    article = await crud_article.update(db, article, article_update)
    return article

@router.delete(
    path="/{article_uuid}",
    status_code=status.HTTP_204_NO_CONTENT,
)
async def delete_article(
    article_uuid: str,
    db: AsyncSession = db_depends,
    user: UserModel = user_depends,
):
    article = await crud_article.get_by_uuid(db, article_uuid)
    if article is None:
        raise not_found
    if article.author_id != user.id:
        raise permission_denied
    await crud_article.delete_from_obj(db, article)
    return
