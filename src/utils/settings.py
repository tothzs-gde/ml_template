from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    '''
    '''
    
    dataset: str
    dataset_test: str

    mlflow_tracking_url: str
    mlflow_experiment_name: str
    mlflow_model_name: str
    mlflow_registered_model_name: str

    minio_url: str
    minio_access_key: str
    minio_secret_key: str
    minio_bucket_name: str

    class Config:
        env_file = "python.env"


settings = Settings()


if __name__ == "__main__":
    settings = Settings()
    print(settings)