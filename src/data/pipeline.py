from collections import OrderedDict
from typing import Callable

import pandas as pd


FEATURES_TO_USE = [
    "Survived",
    "Pclass",
    "Sex",
    "Age",
    "SibSp",
    "Parch",
    "Fare",
    "Embarked",
]


def fill_missing_embarked(df: pd.DataFrame) -> pd.DataFrame:
    df["Embarked"] = df["Embarked"].fillna(df["Embarked"].mode()[0])
    return df


def fill_missing_age(df: pd.DataFrame) -> pd.DataFrame:
    df["Age"] = df["Age"].fillna(df["Age"].median())
    return df


def fill_missing_fare(df: pd.DataFrame) -> pd.DataFrame:
    for p_class in range(1, 4):
        Pclass_median = df[(df["Pclass"] == p_class) & (df["Fare"].notna())][
            "Fare"
        ].median()
        df.loc[
            (df["Pclass"] == p_class) & (df["Fare"].isna() | (df["Fare"] == 0.0)),
            "Fare",
        ] = Pclass_median
    return df


def filter_features(df: pd.DataFrame) -> pd.DataFrame:
    df = pd.DataFrame(df[FEATURES_TO_USE])
    return df


def sex_to_categorical(df: pd.DataFrame) -> pd.DataFrame:
    df["Sex"] = df["Sex"].replace({"male": 0, "female": 1})
    return df


def embarked_to_categorical(df: pd.DataFrame) -> pd.DataFrame:
    df["Embarked"] = df["Embarked"].replace({"S": 0, "C": 1, "Q": 2})
    return df


class Pipeline:
    def __init__(self, steps: list[tuple[str, Callable]]):
        self.length = len(steps)
        self.steps = OrderedDict(steps)

    def process(self, df: pd.DataFrame) -> pd.DataFrame:
        for name, function in self.steps.items():
            print(f"Processing: {name}")
            df = function(df)
        return df


pipe = Pipeline(
    [
        ("fill_missing_embarked", fill_missing_embarked),
        ("fill_missing_age", fill_missing_age),
        ("fill_missing_fare", fill_missing_fare),
        ("filter_features", filter_features),
        ("sex_to_categorical", sex_to_categorical),
        ("embarked_to_categorical", embarked_to_categorical),
    ]
)
