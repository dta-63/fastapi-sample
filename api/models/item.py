
from pydantic import BaseModel


class ItemIn(BaseModel):
    """
    Defined an item for a creation
    """
    name: str


class Item(BaseModel):
    """
    Defined an item model
    """
    id: str
    name: str
    createdBy: str
