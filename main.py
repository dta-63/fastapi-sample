import uvicorn

from fastapi import FastAPI
from api.items import items
from api.others import others


app = FastAPI(
    title="Service example",
    description="Simple api using Fast api framework",
    version="1.0.0"
)

app.include_router(items, prefix="/items", tags=["items"])
app.include_router(others, prefix="/others", tags=["others"])


if __name__ == "__main__":
    uvicorn.run(app, port=8000, loop="asyncio")