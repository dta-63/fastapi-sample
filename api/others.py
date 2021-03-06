from fastapi import APIRouter
from typing import Optional
from cachetools import cached, TTLCache
from api.models.other import Other
from typing import List
from bson import ObjectId


cache = TTLCache(maxsize=100, ttl=300)
others = APIRouter()


@others.get("/", response_model=List[Other])
@cached(cache)
def read_other_data(required: str, optional: Optional[str] = None):
    return [
        {
            "_id": ObjectId("5df9e0fecdd49b0030b58622"),
            "test": "Test 1"
        }
    ]
