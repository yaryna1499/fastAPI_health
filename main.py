from logger import logger
import random
import time
from typing import Optional
import uvicorn
from fastapi import FastAPI, Response
from metrics import PrometheusMiddleware, metrics
from otlp import set_otlp
from config import APP_NAME, EXPOSE_PORT, OTLP_GRPC_ENDPOINT

app = FastAPI()

# Setting metrics middleware
app.add_middleware(PrometheusMiddleware, app_name=APP_NAME)
app.add_route("/metrics", metrics)

# Setting OpenTelemetry
set_otlp(app, APP_NAME, OTLP_GRPC_ENDPOINT)

@app.get("/")
async def read_root():
    logger.error("Hello World")
    return {"Hello": "World"}


@app.get("/items/{item_id}")
async def read_item(item_id: int, q: Optional[str] = None):
    logger.error("items")
    return {"item_id": item_id, "q": q}


@app.get("/io_task")
async def io_task():
    time.sleep(1)
    logger.info("io task")
    return "IO bound task finish!"


@app.get("/cpu_task")
async def cpu_task():
    for i in range(1000):
        _ = i * i * i
    logger.error("cpu task")
    return "CPU bound task finish!"


@app.get("/random_status")
async def random_status(response: Response):
    response.status_code = random.choice([200, 200, 300, 400, 500])
    logger.error("random status")
    return {"path": "/random_status"}


@app.get("/random_sleep")
async def random_sleep(response: Response):
    time.sleep(random.randint(0, 5))
    logger.error("random sleep")
    return {"path": "/random_sleep"}


@app.get("/error_test")
async def error_test(response: Response):
    logger.exception("got error!!!!")
    raise ValueError("value error")


if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=EXPOSE_PORT)
