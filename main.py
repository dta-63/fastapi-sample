import os
import uvicorn

from fastapi import FastAPI, Depends
from logging.config import fileConfig
from dotenv import load_dotenv

from api.items import items
from api.others import others

from tools.mongo_utils import connect, disconnect
from tools.oidc import Auth


load_dotenv()
basedir = os.path.abspath(os.path.dirname(__file__))
fileConfig(os.path.join(basedir, 'logging.ini'), disable_existing_loggers=False)

app = FastAPI(
    title="Service example",
    description="Simple api using Fast api framework",
    version="1.0.0"
)

app.include_router(items, prefix="/items", tags=["items"], dependencies=[Depends(Auth())])
app.include_router(others, prefix="/others", tags=["others"])

app.add_event_handler("startup", connect)
app.add_event_handler("shutdown", disconnect)

if __name__ == "__main__":
    uvicorn.run(app, port=8000, loop="asyncio")
