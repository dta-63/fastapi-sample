import logging
import os

from motor.motor_asyncio import AsyncIOMotorClient


def get_db() -> AsyncIOMotorClient:
    global client
    return client


def connect():
    global client
    logging.info('Mongo connection opening...')
    client = AsyncIOMotorClient(os.getenv('MONGODB_URL'))


def disconnect():
    global client
    logging.info('Mongo connection closing...')
    client.close()
