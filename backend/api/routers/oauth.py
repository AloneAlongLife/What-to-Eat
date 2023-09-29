from sqlalchemy.ext.asyncio import AsyncSession
from fastapi import APIRouter, Depends, Request
from fastapi.security import OAuth2PasswordRequestForm
from pydantic import BaseModel

from ..depends import db_depends
from ..validator import auth_user, refresh_user

class Token(BaseModel):
    access_token: str
    token_type: str

router = APIRouter(
    prefix="/oauth",
    tags=["OAuth"]
)

@router.post("/login", response_model=Token)
async def login(
    request: Request,
    from_data: OAuth2PasswordRequestForm = Depends(),
    db: AsyncSession = db_depends,
) -> Token:
    token = await auth_user(
        ip=request.client.host,
        db=db,
        username=from_data.username,
        password=from_data.username,
    )
    return Token(
        access_token=token,
        token_type="bearer"
    )

@router.get("/refresh", response_model=Token)
async def refresh(new_token: str = Depends(refresh_user)) -> Token:
    return Token(
        access_token=new_token,
        token_type="bearer"
    )
