
from pydantic import BaseModel
from api.models.base import DBModelMixin


class ItemIn(BaseModel):
    """
    Defined an item for a creation
    """
    name: str


class Item(DBModelMixin, ItemIn):
    """
    Defined an item model
    """
    createdBy: str
