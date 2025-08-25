import mlflow
import pandas as pd
from mlflow.models import infer_signature
from sklearn.linear_model import LogisticRegression
from sklearn.preprocessing import MinMaxScaler

from src.data.pipeline import pipe


def train():
    df = pd.read_csv("data/titanic.csv", index_col="PassengerId")
    df = pipe.process(df)

    x = df.drop(columns="Survived")
    y = df["Survived"]

    scaler = MinMaxScaler()
    x = scaler.fit_transform(x)

    params = {
        "solver": "lbfgs",
        "max_iter": 1000,
        "penalty": "l2",
    }
    lr = LogisticRegression(**params)
    lr.fit(x, y)
    score = lr.score(x, y)

    mlflow.set_tracking_uri(uri="http://127.0.0.1:8080")
    mlflow.set_experiment("Titanic PoC")

    with mlflow.start_run():
        mlflow.log_params(params)
        mlflow.log_metric("score", score)

        signature = infer_signature(x, lr.predict(x))

        model_info = mlflow.sklearn.log_model(
            sk_model=lr,
            name="titanic_model",
            signature=signature,
            input_example=x,
            registered_model_name="titanic_model",
        )
        mlflow.set_logged_model_tags(
            model_info.model_id, {"Training Info": "Basic LR model for Titanic dataset"}
        )

    return score
