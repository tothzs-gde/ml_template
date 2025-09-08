import datetime

import mlflow
import pandas as pd
import yaml
from sklearn.metrics import accuracy_score

from src.utils.logging import logger
from src.utils.settings import settings


def evaluate(model_name: str, model_version: str):
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

    run_name = f"eval_{datetime.datetime.now().strftime("%Y%m%d%H%M%S")}"
    logger.info(f"Evaluating model ({model_name}:{model_version})")

    # Load the data
    with open('config/data_config.yaml', 'r') as file:
        metadata = yaml.safe_load(file)

    index_columns = metadata['index_columns']
    target_column = metadata['target_column']

    df_train = pd.read_csv('data/titanic_test.csv', index_col=index_columns)
    X_test = df_train.drop(columns=target_column)
    y_test = df_train[target_column]

    # Load model
    model_name = settings.mlflow_registered_model_name
    model_version = "latest"
    model_uri = f"models:/{model_name}/{model_version}"
    model = mlflow.sklearn.load_model(model_uri)

    # Predict
    with mlflow.start_run(
        run_name=run_name,
        log_system_metrics=True,
        tags={'test_tag': "hello"}
    ):
        y_pred = model.predict(X_test)
        score = accuracy_score(y_test, y_pred)

    return score