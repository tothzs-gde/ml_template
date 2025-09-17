import datetime
from typing import Any

import mlflow
import pandas as pd

from src.data.drift import detect_drift
from src.data.io import import_drift_data
from src.utils.logging import logger
from src.utils.settings import settings


def infer(X_data: list[dict[str, Any]], model_name: str, model_version: str):
    '''
    '''
    mlflow.set_tracking_uri(uri=settings.mlflow_tracking_url)
    mlflow.set_experiment(experiment_name=settings.mlflow_experiment_name)
    mlflow.autolog(
        log_models=False,
    )

    run_name = f"infer_{datetime.datetime.now().strftime("%Y%m%d%H%M%S")}"
    logger.info(f"Predicting with model ({model_name}:{model_version})")

    # Load model
    model_uri = f"models:/{model_name}/{model_version}"
    model = mlflow.sklearn.load_model(model_uri)

    # Data drift detection
    client = mlflow.MlflowClient()
    model_version_details = client.get_model_version(
        name=model_name,
        version=model_version
    )
    tags = model_version_details.tags
    drift_data_file_name = tags.get("drift-data") + '.csv'
    drift_reference_data = import_drift_data(filename=drift_data_file_name)
    drift_results = detect_drift(
        reference_df=drift_reference_data,
        current_df=pd.DataFrame(X_data),
    )
    if len(drift_results):
        for col, result in drift_results.items():
            logger.info(f"{col}: drifted={result['drifted']} (p={result['drift_score']:.4f})")

    # Predict
    predictions = []
    with mlflow.start_run(
        run_name=run_name,
        log_system_metrics=True,
    ):
        for data_point in X_data:
            df = pd.DataFrame([data_point])
            predictions.extend(model.predict(df).tolist())
        
        drifted = False
        for col, results in drift_results.items():
            drifted = drifted and results["drifted"]
            mlflow.log_metric(f"drift_score_{col}", results["drift_score"])
            mlflow.log_metric(f"drift_bool_{col}", results["drifted"])
        
        mlflow.set_tag(f"data_drifted", str(drifted))

    return predictions
