from fastapi import APIRouter

others = APIRouter()

@others.get("/")
async def read_other_data():
    return [{"id": 1, "name": "Test 1"}]
