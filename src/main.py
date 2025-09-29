import json
import time
from contextlib import asynccontextmanager

from fastapi import FastAPI
from fastapi import Request
from fastapi import Response
from uuid_extensions import uuid7

from src.api.api import router
from src.utils.minio import create_drift_bucket
from src.utils.minio import create_mlflow_bucket
from src.utils.logging import request_id_ctx
from src.utils.logging import logger
from src.utils.settings import settings


@asynccontextmanager
async def lifespan(app: FastAPI):
    create_drift_bucket()
    create_mlflow_bucket()
    yield


app = FastAPI(
    lifespan=lifespan,
    docs_url="/docs",
)


@app.middleware("http")
async def log_requests(request: Request, call_next):
    request_id = str(uuid7())
    token = request_id_ctx.set(request_id)
    start_time = time.time()

    try:
        body = await request.json()
    except ValueError:
        body = None

    try:
        response: Response = await call_next(request)
    finally:
        process_time = time.time() - start_time
        log_data = {
            "timestamp": time.strftime("%Y-%m-%d %H:%M:%S", time.gmtime(start_time)),
            "request_id": request_id,
            "path": request.url.path,
            "method": request.method,
            "status_code": response.status_code,
            "process_time_ms": round(process_time * 1000, 2),
            "input_data": body,
            "metadata": {
                "client_host": request.client.host if request.client else None,
                "headers": dict(request.headers),
            }
        }
        logger.info(json.dumps(log_data))
        request_id_ctx.reset(token)

    return response


app.include_router(router)


if __name__ == "__main__":
    import os
    import uvicorn

    os.environ["AWS_ACCESS_KEY_ID"] = settings.aws_access_key_id
    os.environ["AWS_SECRET_ACCESS_KEY"] = settings.aws_secret_access_key
    os.environ["MLFLOW_S3_ENDPOINT_URL"] = f"http://{settings.minio_url}"

    uvicorn.run("src.main:app", host="0.0.0.0", port=8000, reload=True)
