import datetime
from typing import Any

import mlflow
import pandas as pd

from src.utils.logging import logger
from src.utils.settings import settings


def infer(X_data: list[dict[str, Any]], model_name: str, model_version: str):
    '''
    '''
    logger.debug(f"Incoming X_data: {X_data}")
    mlflow.set_tracking_uri(uri=settings.mlflow_tracking_url)
    mlflow.set_experiment(experiment_name=settings.mlflow_experiment_name)
    mlflow.autolog(
        log_models=False,
    )

    run_name = f"infer_{datetime.datetime.now().strftime("%Y%m%d%H%M%S")}"
    logger.info(f"Predicting with model ({model_name}:{model_version})")

    # Load model
    model_name = settings.mlflow_registered_model_name
    model_version = "latest"
    model_uri = f"models:/{model_name}/{model_version}"
    model = mlflow.sklearn.load_model(model_uri)

    # Predict
    predictions = []
    with mlflow.start_run(
        run_name=run_name,
        log_system_metrics=True,
    ):
        for data_point in X_data:
            df = pd.DataFrame([data_point])
            predictions.extend(model.predict(df).tolist())

    return predictions
