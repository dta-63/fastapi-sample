from fastapi import APIRouter, Depends, HTTPException
from typing import List
from api.models.item import Item, ItemIn
from tools.oidc import Auth, User
from tools.mongo import get_db, AsyncIOMotorClient
from bson import ObjectId

items = APIRouter()


@items.get("/", response_model=List[Item])
async def read_items(db: AsyncIOMotorClient = Depends(get_db)):
    # TODO: return _id as id
    return await db.test.test_collection.find().to_list(length=100)


@items.post("/", response_model=Item)
async def create_item(
    item: ItemIn,
    db: AsyncIOMotorClient = Depends(get_db),
    user: User = Depends(Auth(roles=['admin']))
):
    doc = {
        "name": item.name,
        "createdBy": user.given_name
    }
    result = await db.test.test_collection.insert_one(doc)
    return {**doc, "id": str(result.inserted_id)}


@items.get("/{id}", response_model=Item)
async def read_item(id: str, db: AsyncIOMotorClient = Depends(get_db)):
    # TODO: return _id as id
    result = await db.test.test_collection.find_one({"_id": ObjectId(id)})
    if result is None:
        raise HTTPException(status_code=404, detail="Not found")
    return result


@items.put("/{id}", response_model=Item)
async def update_item(
    id: str,
    item: ItemIn,
    db: AsyncIOMotorClient = Depends(get_db),
    user: User = Depends(Auth(roles=['admin']))
):
    doc = {
        "name": item.name,
        "createdBy": user.given_name
    }
    await db.test.test_collection.update_one({"_id": ObjectId(id)}, {'$set': doc})
    return {**doc, "id": id}
