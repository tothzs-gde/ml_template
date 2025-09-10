from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    '''
    '''

    random_seed: int
    test_split_size: float | int
    
    dataset: str
    dataset_test: str

    mlflow_tracking_url: str
    mlflow_experiment_name: str
    mlflow_model_name: str
    mlflow_registered_model_name: str
    mlflow_s3_endpoint_url: str

    minio_url: str
    aws_access_key_id: str
    aws_secret_access_key: str
    minio_mlflow_bucket_name: str
    minio_drift_bucket_name: str

    class Config:
        env_file = "app.env"


settings = Settings()

if __name__ == "__main__":
    settings = Settings()
    print(settings)