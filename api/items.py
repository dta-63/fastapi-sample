from fastapi import APIRouter, Depends, HTTPException
from fastapi.responses import Response
from typing import List
from bson import ObjectId

from api.models.item import Item, ItemIn
from tools.security import Auth, User
from tools.mongo import get_db, AsyncIOMotorClient
from tools.serialization import serialize

items = APIRouter()


@items.get("/", response_model=List[Item])
async def read_items(limit: int = 10, skip: int = 0, db: AsyncIOMotorClient = Depends(get_db)):
    return serialize(
        await db.test.test_collection.find()
                .skip(skip)
                .limit(limit)
                .to_list(length=limit)
    )


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
    if not ObjectId.is_valid(id):
        raise HTTPException(status_code=404, detail="Not found, invalid id")

    result = await db.test.test_collection.find_one({"_id": ObjectId(id)})
    if result is None:
        raise HTTPException(status_code=404, detail="Not found")
    return serialize(result)


@items.delete("/{id}")
async def delete_item(id: str, db: AsyncIOMotorClient = Depends(get_db)):
    if not ObjectId.is_valid(id):
        raise HTTPException(status_code=404, detail="Not found, invalid id")

    result = await db.test.test_collection.delete_one({"_id": ObjectId(id)})
    if result is None:
        raise HTTPException(status_code=404, detail="Not found")
    return Response(status_code=204)


@items.put("/{id}", response_model=Item)
async def update_item(
    id: str,
    item: ItemIn,
    db: AsyncIOMotorClient = Depends(get_db),
    user: User = Depends(Auth(roles=['admin']))
):
    if not ObjectId.is_valid(id):
        raise HTTPException(status_code=404, detail="Not found, invalid id")
    doc = {
        "name": item.name,
        "createdBy": user.given_name
    }
    await db.test.test_collection.update_one({"_id": ObjectId(id)}, {'$set': doc})
    return {**doc, "id": id}
