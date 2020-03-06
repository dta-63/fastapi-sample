import os
import uvicorn

from fastapi import FastAPI
from dotenv import load_dotenv
load_dotenv()

from api import router as api_router
from api.consumers import items_consumer_callback
from tools import kafka, mongo

app = FastAPI(
    title="SERVICE_NAME",
    description="SERVICE_DESCRIPTION",
    debug=os.getenv("DEBUG", "0"),
    version=os.getenv("VERSION", "1.0.0"),
    openapi_prefix=os.getenv("ROOT_PATH", "")
)

app.include_router(api_router)


@app.on_event("startup")
def startup_event():
    mongo.connect()
    kafka.create_producer()
    kafka.add_consumer(['items'], items_consumer_callback)


@app.on_event("shutdown")
def shutdown_event():
    mongo.disconnect()
    kafka.close()


if __name__ == "__main__":
    uvicorn.run(
        "main:app",
        host="0.0.0.0",
        port=8080,
        proxy_headers=True,
        lifespan="on",
        root_path=os.getenv("ROOT_PATH", ""),
        log_level=os.getenv("LOG_LEVEL", "debug")
    )
