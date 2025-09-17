import datetime

import mlflow
import pandas as pd
import yaml
from sklearn.metrics import classification_report

from src.utils.logging import logger
from src.utils.settings import settings


def evaluate(
    model_name: str,
    model_version: str,
    data_config_path: str = "config/data_config.yaml",
    test_data_path: str = "data/titanic_test.csv",
    run_id: str = None,
    run_name: str = None,
):
    '''
    '''
    mlflow.set_tracking_uri(uri=settings.mlflow_tracking_url)
    mlflow.set_experiment(experiment_name=settings.mlflow_experiment_name)
    mlflow.autolog(
        log_input_examples=True,
        log_model_signatures=True,
        log_models=True,
        log_datasets=True,
        log_traces=True,
    )

    if run_name is None:
        run_name = f"eval_{datetime.datetime.now().strftime("%Y%m%d%H%M%S")}"
    logger.info(f"Evaluating model ({model_name}:{model_version})")

    # Load the data
    with open(data_config_path, 'r') as file:
        metadata = yaml.safe_load(file)

    index_columns = metadata['index_columns']
    target_column = metadata['target_column']

    df_train = pd.read_csv(test_data_path, index_col=index_columns)
    X_test = df_train.drop(columns=target_column)
    y_test = df_train[target_column]

    # Load model
    model_uri = f"models:/{model_name}/{model_version}"
    model = mlflow.sklearn.load_model(model_uri)

    # Predict
    with mlflow.start_run(
        run_id=run_id,
        run_name=run_name,
        log_system_metrics=True,
    ):
        y_pred = model.predict(X_test)
        report = classification_report(y_test, y_pred, output_dict=True)
        logger.info(report)

        out = {
            "accuracy": report["accuracy"],
            "precision": report["weighted avg"]["precision"],
            "recall": report["weighted avg"]["recall"],
            "f1-score": report["weighted avg"]["f1-score"],
        }

        mlflow.log_metric("eval_accuracy_score", out["accuracy"])
        mlflow.log_metric("eval_precision_score", out["precision"])
        mlflow.log_metric("eval_recall_score", out["recall"])
        mlflow.log_metric("eval_f1_score", out["f1-score"])

    return out