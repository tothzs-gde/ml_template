import json
import time
from contextlib import asynccontextmanager

from fastapi import FastAPI
from fastapi import Request
from fastapi import Response
from fastapi.responses import JSONResponse
from uuid_extensions import uuid7

from src.api.api import router
from src.utils.minio import create_drift_bucket
from src.utils.minio import create_mlflow_bucket
from src.utils.logging import correlation_id_ctx
from src.utils.logging import logger
from src.utils.settings import settings


@asynccontextmanager
async def lifespan(app: FastAPI):
    create_drift_bucket()
    create_mlflow_bucket()
    yield


app = FastAPI(
    title="ML Template",
    description="Template API application for running ML models",
    lifespan=lifespan,
    docs_url="/docs",
)


@app.middleware("http")
async def log_requests_middleware(request: Request, call_next):
    start_time = time.time()

    corr_id = request.headers.get("X-Correlation-ID", str(uuid7()))
    token = correlation_id_ctx.set(corr_id)

    try:
        try:
            response: Response = await call_next(request)
        except Exception as e:
            logger.exception("Unhandled exception in request")
            response = JSONResponse(
                status_code=500,
                content={"detail": "Internal Server Error"},
            )
        response.headers["X-Correlation-ID"] = corr_id
    finally:
        process_time = time.time() - start_time
        log_data = {
            "path": request.url.path,
            "method": request.method,
            "status_code": response.status_code,
            "process_time_ms": round(process_time * 1000, 2),
            "client_host": request.client.host,
            "headers": dict(request.headers),
        }
        logger.info("Request completed", extra={"extra_data": log_data})
        correlation_id_ctx.reset(token)

    return response


app.include_router(router)


if __name__ == "__main__":
    import os
    import uvicorn

    os.environ["AWS_ACCESS_KEY_ID"] = settings.aws_access_key_id
    os.environ["AWS_SECRET_ACCESS_KEY"] = settings.aws_secret_access_key
    os.environ["MLFLOW_S3_ENDPOINT_URL"] = f"http://{settings.minio_url}"

    uvicorn.run("src.main:app", host="0.0.0.0", port=8000, reload=True)
