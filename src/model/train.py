import datetime

import mlflow
from sklearn.model_selection import train_test_split

from src.data.datasource import load_from_csv
from src.data.drift import export_drift_data
from src.model import RANDOM_SEED
from src.utils.logging import logger
from src.utils.settings import settings


def train(model_name: str, model_version: str):
    ''' 
    '''

    mlflow.set_tracking_uri(uri=settings.mlflow_tracking_url)
    mlflow.set_experiment(experiment_name=settings.mlflow_experiment_name)
    mlflow.autolog(
        log_input_examples=True,
        log_model_signatures=True,
        log_models=False,
        log_datasets=True,
        log_traces=True,
    )
    
    run_name = f"train_{datetime.datetime.now().strftime("%Y%m%d%H%M%S")}"
    logger.info(f"Start to train a new model ({model_name}) under {run_name=}")

    X_data, y_data = load_from_csv(
        data_path='data/titanic.csv',
        config_path="config/data_config.yaml",
    )

    X_train, X_drift = train_test_split(
        X_data,
        test_size=settings.test_split_size,
        random_state=RANDOM_SEED,
    )
    y_train, y_drift = train_test_split(
        y_data,
        test_size=settings.test_split_size,
        random_state=RANDOM_SEED,
    )

    drift_file_name = export_drift_data(X_drift, y_drift)

    model_name = settings.mlflow_registered_model_name
    model_version = "latest"
    model_uri = f"models:/{model_name}/{model_version}"
    model = mlflow.sklearn.load_model(model_uri)

    tags = {
        "drift-data": drift_file_name
    }

    with mlflow.start_run(
        run_name=run_name,
        log_system_metrics=True,
        tags=tags,
    ):
        model.fit(X_train, y_train)
        model_info = mlflow.sklearn.log_model(
            sk_model=model,
            name=settings.mlflow_model_name,
            input_example=X_train.head(),
            registered_model_name=settings.mlflow_registered_model_name,
        )
        
    logger.info(f"Training completed: {model_name}")

    return (
        run_name,
        settings.mlflow_registered_model_name,
        model_info.registered_model_version
    )
