
from pydantic import BaseModel
from api.models.db import DBModelMixin


class ItemIn(BaseModel):
    """
    Defined an item for a creation
    """
    name: str


class Item(DBModelMixin):
    """
    Defined an item model
    """
    name: str
    createdBy: str
