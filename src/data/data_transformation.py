import pandas as pd

from src.data import Pipeline


def sex_to_categorical(df: pd.DataFrame) -> pd.DataFrame:
    df["Sex"] = df["Sex"].replace({"male": 0, "female": 1})
    return df


def embarked_to_categorical(df: pd.DataFrame) -> pd.DataFrame:
    df["Embarked"] = df["Embarked"].replace({"S": 0, "C": 1, "Q": 2})
    return df


data_transformation_pipeline = Pipeline([
    ("sex_to_categorical", sex_to_categorical),
    ("embarked_to_categorical", embarked_to_categorical),
])