import mlflow
import pandas as pd
from sklearn.preprocessing import MinMaxScaler

from src.data.pipeline import pipe


def infer():
    print("hello")
    df = pd.read_csv("data/titanic_test.csv", index_col="PassengerId")
    df = pipe(df)

    x = df.drop(columns="Survived")

    # This gotta be packaged with the models at train time or even better if
    # it is part of the data preprocessing pipeline
    scaler = MinMaxScaler()
    x = scaler.fit_transform(x)

    model_name = "sklearn-logreg-model"
    model_version = "latest"
    model_uri = f"models:/{model_name}/{model_version}"
    model = mlflow.sklearn.load_model(model_uri)
    y_pred = model.predict(x[:1])

    return y_pred.tolist()
