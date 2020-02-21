import logging
from fastapi import APIRouter, Depends

from api.models.item import Item
from tools.oidc import Auth, User

items = APIRouter()


@items.get("/")
async def read_items(user: User = Depends(Auth(roles=['admin']))):
    logging.info("Hello {}".format(user.given_name))
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
