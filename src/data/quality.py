import pandas as pd
import yaml
from evidently import Dataset
from evidently import DataDefinition
from evidently import Report
from evidently.presets import DatasetStats

from src.utils.logging import logger

def check_data_quality(
    df: pd.DataFrame,
):
    with open("config/data_config.yaml", 'r') as file:
        metadata = yaml.safe_load(file)

    schema = DataDefinition(
        numerical_columns=metadata['numerical_features'],
        categorical_columns=metadata['categorical_features'],
    )

    X = Dataset.from_pandas(
        df,
        data_definition=schema,
    )

    report = Report([
        DatasetStats(),
    ])

    evaluation = report.run(X)

    metric_mapping = {
        "RowCount()": "row_count",
        "ColumnCount()": "column_count",
        "ColumnCount(column_type=ColumnType.Numerical)": "numerical_column_count",
        "ColumnCount(column_type=ColumnType.Categorical)": "categorical_column_count",
        "ColumnCount(column_type=ColumnType.Datetime)": "datetime_column_count",
        "ColumnCount(column_type=ColumnType.Text)": "text_column_count",
        "DuplicatedRowCount()": "duplicated_row_count",
        "DuplicatedColumnsCount()": "duplicated_columns_count",
        "AlmostDuplicatedColumnsCount()": "almost_duplicated_columns_count",
        "AlmostConstantColumnsCount()": "almost_constant_columns_count",
        "EmptyRowsCount()": "empty_rows_count",
        "EmptyColumnsCount()": "empty_columns_count",
        "ConstantColumnsCount()": "constant_columns_count",
        "DatasetMissingValueCount()": "dataset_missing_value_count", 
    }

    for metric in evaluation.dict()['metrics']:
        if metric["metric_id"] == "DatasetMissingValueCount()":
            data = {
                "quality_test": "evidently",
                "metric": metric_mapping[metric["metric_id"]],
                "value": metric['value']['count']
            }
        else:
            data = {
                "quality_test": "evidently",
                "metric": metric_mapping[metric["metric_id"]],
                "value": metric['value']
            }
        logger.info("Data quality check", extra={"extra_data": data})
