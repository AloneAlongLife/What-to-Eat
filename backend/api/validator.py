from fastapi import Depends, HTTPException, Request, status
from fastapi.security import OAuth2PasswordBearer
from jwt import decode, encode
from jwt.exceptions import PyJWTError
from sqlalchemy.ext.asyncio import AsyncSession

from datetime import datetime, timedelta
from typing import Any

from config import KEY
from crud import CRUDUser
from database.database import get_session
from models import UserModel
from swap import CHANGE_PASSWORD_USER
from utils import password_hash

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="oauth/login")
curd_user = CRUDUser()

unauthorize = HTTPException(
    status_code=status.HTTP_401_UNAUTHORIZED,
    detail="Could not validate token.",
)
authorize_fail = HTTPException(
    status_code=status.HTTP_401_UNAUTHORIZED,
    detail="Incorrect username or password.",
)
different_ip = HTTPException(
    status_code=status.HTTP_403_FORBIDDEN,
    detail="Different IP detected.",
)

async def get_current_user(
    request: Request,
    token: str = Depends(oauth2_scheme),
    db: AsyncSession = Depends(get_session),
) -> UserModel:
    try:
        data: dict[str, Any] = decode(
            token,
            KEY,
            algorithms="HS256",
            options={
                "require": ["exp", "iat", "address"]
            }
        )
    except PyJWTError:
        raise unauthorize
    # 登入設備不同
    ip = data.get("address")
    if request.client.host != ip:
        raise different_ip
    username = data.get("sub")
    if not username:
        raise unauthorize
    # 更改密碼，憑證失效
    iat = data["iat"]
    if iat < CHANGE_PASSWORD_USER.get(username, 0):
        raise unauthorize
    # 檢查用戶
    user = await curd_user.get_by_username(db, username)
    if not user:
        raise unauthorize
    return user

async def auth_user(
    db: AsyncSession,
    username: str,
    password: str,
    ip: str,
) -> str:
    user = await curd_user.get_by_username(db, username)
    if not user:
        raise authorize_fail
    hash_password = password_hash(password)
    if hash_password != user.hashpassword or user.disable:
        raise authorize_fail
    return encode(
        {
            "sub": username,
            "address": ip,
            "iat": datetime.utcnow(),
            "exp": datetime.utcnow() + timedelta(days=1),
        },
        key=KEY,
        algorithm="HS256"
    )

async def refresh_user(
    request: Request,
    token: str = Depends(oauth2_scheme),
) -> str:
    try:
        data: dict = decode(
            token,
            key=KEY,
            algorithms="HS256",
            options={
                "require": ["exp", "iat", "sub", "address"],
                "verify_exp": False
            }
        )
    except:
        raise unauthorize

    # 不同設備
    ip = data.get("address")
    if request.client.host != ip:
        raise different_ip
    
    username = data.get("sub")
    if not username:
        raise unauthorize
    # 更改密碼，憑證失效
    iat = datetime.fromtimestamp(data["iat"])
    if iat < CHANGE_PASSWORD_USER.get(username, 0):
        raise unauthorize
    
    # 超過一天未登入
    now_exp = datetime.fromtimestamp(data["exp"])
    if datetime.utcnow() - now_exp > timedelta(days=1):
        raise unauthorize
    data["iat"] = datetime.utcnow()
    data["exp"] = datetime.utcnow() + timedelta(days=1)
    return encode(
        data,
        key=KEY,
        algorithm="HS256"
    )
