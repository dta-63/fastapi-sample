import logging
import os

from motor.motor_asyncio import AsyncIOMotorClient

logger = logging.getLogger(__name__)


class DataBase:
    client: AsyncIOMotorClient = None


db = DataBase()


async def get_db() -> AsyncIOMotorClient:
    return db.client


async def connect():
    logger.info('Mongo connection starting...')
    db.client = AsyncIOMotorClient(os.getenv('MONGODB_URL'))


async def disconnect():
    logger.info('Mongo connection ending...')
    db.client.close()
