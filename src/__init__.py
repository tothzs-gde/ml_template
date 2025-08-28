import os

from minio import Minio
from minio.error import S3Error

from src.utils.settings import settings


os.environ["AWS_ACCESS_KEY_ID"] = settings.minio_access_key
os.environ["AWS_SECRET_ACCESS_KEY"] = settings.minio_secret_key
os.environ["MLFLOW_S3_ENDPOINT_URL"] = f"http://{settings.minio_url}"


client = Minio(
    settings.minio_url,
    access_key=settings.minio_access_key,
    secret_key=settings.minio_secret_key,
    secure=False,
)

if not client.bucket_exists(settings.minio_bucket_name):
    client.make_bucket(settings.minio_bucket_name)


try:
    result = client.fput_object(
        bucket_name=settings.minio_bucket_name,
        object_name=f"datasets/titanic.csv",
        file_path=f"data/titanic.csv",
        content_type="application/csv"
    )
    print("Upload successful:")
    print(f"- Object: {result.object_name}")
    print(f"- ETag: {result.etag}")
except S3Error as err:
    print(f"Upload failed: {err}")
