import os
import uvicorn

from fastapi import FastAPI
from logging.config import fileConfig
from dotenv import load_dotenv
from api import router as api_router
from tools.mongo import connect, disconnect
from tools.exceptions import http_error_handler
from starlette.exceptions import HTTPException


load_dotenv()
basedir = os.path.abspath(os.path.dirname(__file__))
fileConfig(os.path.join(basedir, 'logging.ini'), disable_existing_loggers=False)

app = FastAPI(
    title="SERVICE_NAME",
    description="SERVICE_DESCRIPTION",
    version=os.getenv('SERVICE_VERSION')
)

app.add_exception_handler(HTTPException, http_error_handler)

app.include_router(api_router)

app.add_event_handler("startup", connect)
app.add_event_handler("shutdown", disconnect)

if __name__ == "__main__":
    uvicorn.run(app, port=8000, loop="asyncio")
