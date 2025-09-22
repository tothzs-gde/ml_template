from minio import Minio

from src.utils.logging import logger
from src.utils.settings import settings


minio_client = Minio(
    settings.minio_url,
    access_key=settings.aws_access_key_id,
    secret_key=settings.aws_secret_access_key,
    secure=False,
)


def create_mlflow_bucket():
    if not minio_client.bucket_exists(settings.minio_mlflow_bucket_name):
        logger.info("MLflow bucket doesn't exist. Creating...")
        minio_client.make_bucket(settings.minio_mlflow_bucket_name)
    else:
        logger.info("Using existing MLflow bucket")


def create_drift_bucket():
    if not minio_client.bucket_exists(settings.minio_drift_bucket_name):
        logger.info("Drift bucket doesn't exist. Creating...")
        minio_client.make_bucket(settings.minio_drift_bucket_name)
    else:
        logger.info("Using existing Drift bucket")
