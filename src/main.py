from contextlib import asynccontextmanager
import os

from fastapi import FastAPI

from src.api.api import router
from src.utils.minio import create_mlflow_bucket
from src.utils.settings import settings


@asynccontextmanager
async def lifespan(app: FastAPI):
    create_mlflow_bucket()
    yield


app = FastAPI(
    lifespan=lifespan,
    docs_url="/docs",
)


app.include_router(router)


if __name__ == "__main__":
    import os
    import uvicorn

    os.environ["AWS_ACCESS_KEY_ID"] = settings.aws_access_key_id
    os.environ["AWS_SECRET_ACCESS_KEY"] = settings.aws_secret_access_key
    os.environ["MLFLOW_S3_ENDPOINT_URL"] = f"http://{settings.minio_url}"

    uvicorn.run("src.main:app", host="0.0.0.0", port=8000, reload=True)