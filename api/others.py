from fastapi import APIRouter
from typing import Optional

others = APIRouter()


@others.get("/")
async def read_other_data(required: str, optional: Optional[str] = None):
    return [{"id": 1, "name": "Test 1"}]
