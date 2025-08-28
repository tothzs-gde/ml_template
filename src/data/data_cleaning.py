import pandas as pd

from src.data import Pipeline


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


data_cleaning_pipeline = Pipeline([
    ("fill_missing_embarked", fill_missing_embarked),
    ("fill_missing_age", fill_missing_age),
    ("fill_missing_fare", fill_missing_fare),
])