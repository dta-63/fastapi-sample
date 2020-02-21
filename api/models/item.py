
from pydantic import BaseModel


class ItemIn(BaseModel):
    name: str


class Item(BaseModel):
    id: str
    name: str
    createdBy: str
