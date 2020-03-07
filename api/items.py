from fastapi import APIRouter, Depends, HTTPException
from fastapi.responses import Response, JSONResponse
from fastapi.encoders import jsonable_encoder

from typing import List
from bson import ObjectId

from api.models.item import Item, ItemIn
from tools.security import Auth, User
from tools.mongo import get_db, AsyncIOMotorClient
# from tools.kafka import get_producer, Producer, KafkaException

items = APIRouter()
# producer_kafka_topic = "items"


@items.get("/", response_model=List[Item])
async def read_items(limit: int = 10, skip: int = 0, db: AsyncIOMotorClient = Depends(get_db)):
    items = map(
        lambda x: Item(**x),
        await db.test.test_collection.find().skip(skip).limit(limit).to_list(length=limit)
    )
    return JSONResponse(content=jsonable_encoder(list(items), by_alias=False))


@items.post("/", response_model=Item)
async def create_item(
    item: ItemIn,
    db: AsyncIOMotorClient = Depends(get_db),
    # producer: Producer = Depends(get_producer),
    user: User = Depends(Auth(roles=['admin']))
):
    doc = {
        "name": item.name,
        "createdBy": user.given_name
    }

    await db.test.test_collection.insert_one(doc)
    item = jsonable_encoder(Item(**doc), by_alias=False)
    # Example to produce on kafka stream
    # try:
    #     producer.produce(producer_kafka_topic, item)
    # except KafkaException as ex:
    #     raise HTTPException(status_code=500, detail=ex.args[0].str())

    return JSONResponse(content=item)


@items.get("/{id}", response_model=Item)
async def read_item(id: str, db: AsyncIOMotorClient = Depends(get_db)):
    if not ObjectId.is_valid(id):
        raise HTTPException(status_code=404, detail="Not found, invalid id")

    item = await db.test.test_collection.find_one({"_id": ObjectId(id)})
    if item is None:
        raise HTTPException(status_code=404, detail="Not found")
    return JSONResponse(content=jsonable_encoder(Item(**item), by_alias=False))


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

    query = {
        "_id": ObjectId(id)
    }
    await db.test.test_collection.update_one(query, {'$set': doc})
    item = {**doc, **query}
    return JSONResponse(content=jsonable_encoder(Item(**item), by_alias=False))
