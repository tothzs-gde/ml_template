import os

from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    '''
    '''

    random_seed: int = 42
    drift_split_size: float | int = 0.1
    
    dataset: str
    dataset_test: str

    mlflow_tracking_url: str = "http://mlflow:8080"
    mlflow_experiment_name: str = "Titanic PoC"
    mlflow_model_name: str = "titanic_model"
    mlflow_registered_model_name: str = "sklearn-logreg-model"
    mlflow_s3_endpoint_url: str = "http://minio:9000"

    minio_url: str = "minio:9000"
    aws_access_key_id: str = "minioadmin"
    aws_secret_access_key: str = "minioadmin"
    minio_mlflow_bucket_name: str = "mlflow"
    minio_drift_bucket_name: str = "driftdata"

    postgres_db: str = "postgres"
    postgres_user: str = "user"
    postgres_password: str = "password"
    postgres_port: int = 5432

    class Config:
        env_file = \
            "../manual.env" \
            if os.getcwd().split("/")[-1] == "notebooks" \
            else "manual.env"


settings = Settings()
