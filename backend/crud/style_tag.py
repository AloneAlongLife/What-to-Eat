from models import StyleTagModel
from schemas import StyleTag, StyleTagCreate, StyleTagUpdate

from .base import CRUDBase

class CRUDStyleTag(CRUDBase[StyleTagModel, StyleTag, StyleTagCreate, StyleTagUpdate]):
    def __init__(self) -> None:
        super().__init__(StyleTagModel)