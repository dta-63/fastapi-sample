from fastapi import APIRouter
from pydantic import BaseModel

items = APIRouter()


class Item(BaseModel):
    name: str

@items.get("/")
async def read_items():
    return [{"id": 1, "name": "Test 1"}, {"id": 2, "name": "Test 2"}]

@items.post("/")
async def create_item(item: Item):
    return {"name": item.name, "id": 3}

@items.get("/{id}")
async def read_item(id: int):
    return {"id": id}

@items.put("/{id}")
async def update_item(id: int, item: Item):
    return {"name": item.name, "id": id}