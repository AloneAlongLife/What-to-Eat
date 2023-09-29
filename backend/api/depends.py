from fastapi import Depends

from database.database import get_session

from .validator import get_current_user

db_depends = Depends(get_session)
user_depends = Depends(get_current_user)
