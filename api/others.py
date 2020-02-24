from fastapi import APIRouter
from typing import Optional
from cachetools import cached, TTLCache


cache = TTLCache(maxsize=100, ttl=300)
others = APIRouter()


@others.get("/")
@cached(cache)
def read_other_data(required: str, optional: Optional[str] = None):
    return [{"id": 1, "name": "Test 1"}]


@others.post("/")
def post_other_data():
    return [{"id": 1, "name": "Test 1"}]
