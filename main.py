import uvicorn

from fastapi import FastAPI
from pydantic import BaseModel

app = FastAPI(
    title="Service example",
    description="Simple api using Fast api framework",
    version="1.0.0"
)


class Item(BaseModel):
    name: str


@app.get("/items/{id}")
async def read_item(id: int):
    return {"id": id}

@app.put("/items/{id}")
async def update_item(id: int, item: Item):
    return {"name": item.name, "id": id}


if __name__ == "__main__":
    uvicorn.run(app, port=8000, loop="asyncio")