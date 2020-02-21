import logging

import os
from motor.motor_asyncio import AsyncIOMotorClient, AsyncIOMotorDatabase
from tools.mongo import db


async def get_client() -> AsyncIOMotorClient:
    return db.client


async def get_database(database: str) -> AsyncIOMotorDatabase:
    return db.client[database]


async def connect():
    logging.info('Mongo connection starting...')
    db.client = AsyncIOMotorClient(os.getenv('MONGODB_URL'))


async def disconnect():
    logging.info('Mongo connection ending...')
    db.client.close()
