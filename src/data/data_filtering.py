import pandas as pd

from src.data import Pipeline
from src.utils.settings import settings


def filter_features(df: pd.DataFrame) -> pd.DataFrame:
    df = pd.DataFrame(df[settings.features_to_use])
    return df


data_filtering_pipeline = Pipeline([
    ("filter_features", filter_features),
])