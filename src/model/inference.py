import datetime
from typing import Any

import mlflow
import pandas as pd

from src.data.drift import detect_drift_manual
from src.data.drift import detect_drift_model_based
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
    drift_results = detect_drift_manual(
        reference_df=drift_reference_data,
        subject_df=pd.DataFrame(X_data),
    )
    if len(drift_results):
        for col, result in drift_results.items():
            logger.info(f"{col}: drifted={result['drifted']} (p={result['drift_score']:.4f})")
    detect_drift_model_based(
        reference_df=drift_reference_data,
        subject_df=pd.DataFrame(X_data),
    )

    # Predict
    out = []
    with mlflow.start_run(
        run_name=run_name,
        log_system_metrics=True,
    ):
        for data_point in X_data:
            row_df = pd.DataFrame([data_point])
            pred = model.predict(row_df)[0]
            prob = model.predict_proba(row_df)[0]

            out.append({
                "prediction": int(pred),
                "probabilities": prob.tolist(),
            })
        
        drifted = False
        for col, results in drift_results.items():
            drifted = drifted and results["drifted"]
            mlflow.log_metric(f"drift_{col}_bool", results["drifted"])
            mlflow.log_metric(f"drift_{col}_score", results["drift_score"])
        
        mlflow.set_tag(f"data_drifted", str(drifted))

    logger.info("============================")
    logger.info(out)

    return out
