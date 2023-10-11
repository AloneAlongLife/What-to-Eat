from aiofile import async_open
from fastapi import APIRouter, HTTPException, status, UploadFile

from models import UserModel

from base64 import b64decode, b64encode
from os import remove
from os.path import isfile
from time import time
from typing import List

from config import DATA_DIR

from ..depends import user_depends

permission_denied = HTTPException(
    status_code=status.HTTP_403_FORBIDDEN,
    detail="Permission denied."
)
file_not_found = HTTPException(
    status_code=status.HTTP_404_NOT_FOUND,
    detail="File not found.",
)

router = APIRouter(
    prefix="/image",
    tags=["Image"],
)
IMAGE_DIR = lambda x: f"{DATA_DIR}/image/{x}"

@router.post(
    "/",
    status_code=status.HTTP_201_CREATED,
)
async def upload_file(
    files: List[UploadFile],
    user: UserModel = user_depends,
):
    result = []
    for i, file in enumerate(files):
        filename = b64encode(f"{user.uuid}-{i}{time()}".encode("utf-8")).hex()
        content = await file.read()

        async with async_open(IMAGE_DIR(filename), "wb") as ifp:
            await ifp.write(content)
        result.append(filename)
    return result

@router.delete(
    "/{image_name}",
    status_code=status.HTTP_204_NO_CONTENT,
)
async def delete_file(
    image_name: str,
    user: UserModel = user_depends,
):
    if not isfile(IMAGE_DIR(image_name)):
        raise file_not_found
    real_image_name = b64decode(bytes.fromhex(image_name)).decode("utf-8")
    if not real_image_name.startswith(f"{user.uuid}-"):
        raise permission_denied
    remove(IMAGE_DIR(image_name))
    
