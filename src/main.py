from contextlib import asynccontextmanager

from fastapi import FastAPI
from minio import Minio

from src.api.api import router
from src.utils.logging import logger
from src.utils.settings import settings


def setup_minio_bucket():
    client = Minio(
        settings.minio_url,
        access_key=settings.aws_access_key_id,
        secret_key=settings.aws_secret_access_key,
        secure=False,
    )

    if not client.bucket_exists(settings.minio_bucket_name):
        logger.info("MLflow bucket doesn't exist. Creating...")
        client.make_bucket(settings.minio_bucket_name)
    else:
        logger.info("Using existing MLflow bucket")


@asynccontextmanager
async def lifespan(app: FastAPI):
    setup_minio_bucket()
    yield


app = FastAPI(
    lifespan=lifespan,
    docs_url="/docs",
)


app.include_router(router)
