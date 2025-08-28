from src.data import Pipeline
from src.data.data_cleaning import data_cleaning_pipeline
from src.data.data_transformation import data_transformation_pipeline
from src.data.data_filtering import data_filtering_pipeline


pipe = Pipeline(
    [
        ("data_cleaning_pipeline", data_cleaning_pipeline),
        ("data_filtering_pipeline", data_filtering_pipeline),
        ("data_transformation_pipeline", data_transformation_pipeline),
    ]
)
