from fastapi import APIRouter, Depends, HTTPException
from fastapi.responses import Response

from typing import List
from bson import ObjectId
from bson.errors import InvalidId

from api.models.item import Item, ItemIn
from tools.security import Auth, User
from tools.mongo import get_db, AsyncIOMotorClient
# from tools.kafka import get_producer, Producer, KafkaException

items = APIRouter()
# producer_kafka_topic = "items"


@items.get("/", response_model=List[Item])
async def read_items(
    limit: int = 10,
    skip: int = 0,
    db: AsyncIOMotorClient = Depends(get_db)
):
    return await db.test.test_collection.find().skip(skip).limit(limit).to_list(length=limit)


@items.post("/", response_model=Item, status_code=201)
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
    item = Item(**doc)
    # Example to produce on kafka stream
    # try:
    #     producer.produce(producer_kafka_topic, item)
    # except KafkaException as ex:
    #     raise HTTPException(status_code=500, detail=ex.args[0].str())

    return item


@items.get("/{id}", response_model=Item)
async def read_item(
    id: str,
    db: AsyncIOMotorClient = Depends(get_db)
):
    if not ObjectId.is_valid(id):
        raise HTTPException(status_code=404, detail="Not found, invalid id")

    item = await db.test.test_collection.find_one({"_id": ObjectId(id)})
    if item is None:
        raise HTTPException(status_code=404, detail="Not found")
    return item


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
    return {**doc, **query}


@items.delete("/{ids}")
async def delete_items(
    ids: str,
    db: AsyncIOMotorClient = Depends(get_db)
):
    try:
        ids = list(map(lambda x: ObjectId(x), ids.split(',')))
    except InvalidId:
        raise HTTPException(status_code=404, detail="Not found, invalid id list")

    result = await db.test.test_collection.delete_many({"_id": {"$in": ids}})
    if result.deleted_count == 0:
        raise HTTPException(status_code=404, detail="Not found")
    return Response(status_code=204)
