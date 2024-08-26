"""Entrypoint to invoke the FastAPI application service with."""

from fastapi import FastAPI, status
from pydantic import BaseModel
import uvicorn
from multiprocessing import Queue
from logging_loki import LokiQueueHandler
import logging
from starlette_exporter import PrometheusMiddleware, handle_metrics


app = FastAPI()
app.add_middleware(PrometheusMiddleware, app_name="hello_world", skip_paths=["/metrics"])
app.add_route("/metrics", handle_metrics)


loki_logs_handler = LokiQueueHandler(
    Queue(-1),
    url="http://18.235.248.167:3100/loki/api/v1/push",
    tags={"application": "fastapi"},
    version="1",
)

uvicorn_access_logger = logging.getLogger("uvicorn.access")
uvicorn_access_logger.addHandler(loki_logs_handler)


class HealthCheck(BaseModel):
    """Response model to validate and return when performing a health check."""

    status: str = "OK"


@app.get(
    "/health",
    tags=["healthcheck"],
    summary="Perform a Health Check",
    response_description="Return HTTP Status Code 200 (OK)",
    status_code=status.HTTP_200_OK,
    response_model=HealthCheck,
)
def get_health() -> HealthCheck:
    """
    ## Perform a Health Check
    Endpoint to perform a healthcheck on. This endpoint can primarily be used Docker
    to ensure a robust container orchestration and management is in place. Other
    services which rely on proper functioning of the API service will not deploy if this
    endpoint returns any other HTTP status code except 200 (OK).
    Returns:
        HealthCheck: Returns a JSON response with the health status
    """
    logging.error("test error")
    return HealthCheck(status="OK")


def main() -> None:
    """Entrypoint to invoke when this module is invoked on the remote server."""
    # See the official documentations on how "0.0.0.0" makes the service available on
    # the local network - https://www.uvicorn.org/settings/#socket-binding
    uvicorn.run("main:app", host="0.0.0.0")


if __name__ == "__main__":
    main()

"""
To check if the API service works as expected, perform the following actions:
    1. Run the API service by invoking this command - "python -m main".
    2. If the service is running, open the URL "http://localhost:8000" in your browser.
    3. With cURL, invoke this command:
       "curl --include --request GET "http://localhost:8000/health" and you should
       get a HTTP Status Code 200 OK message somewhere in it."
An example Dockerfile with a healthcheck capabilities enabled is available in this gist:
https://gist.github.com/Jarmos-san/11bf22c59d26daf0aa5223bdd50440da
"""