from io import BytesIO

import pandas as pd
import yaml
from uuid_extensions import uuid7str

from src.utils.logging import logger
from src.utils.minio import create_drift_bucket
from src.utils.minio import minio_client
from src.utils.settings import settings


def load_from_csv(data_path: str, config_path: str) -> tuple[pd.DataFrame]:
    ''' Imports the .csv file given by the path argument.

    Args:
        path: Path to the .csv file relative to the project's root folder.

    Returns:
        tuple[pd.DataFrame]: Separated input and target dataframes of the 
            imported file.
    '''

    logger.info(f'Importing data from local csv: {data_path}')

    with open(config_path, 'r') as file:
        metadata = yaml.safe_load(file)

    index_columns = metadata['index_columns']
    target_column = metadata['target_column']

    df = pd.read_csv(data_path, index_col=index_columns)
    X_data = df.drop(columns=target_column)
    y_data = df[target_column]

    logger.info(f'Imported dataset {df.shape}')

    return X_data, y_data


def export_drift_data(
    X_drift: pd.DataFrame,
    y_drift: pd.DataFrame = None,
) -> str:
    ''' Export the combined input (X_drift) and target (y_drift) data to the 
    MinIO S3 drift bucket. The exported data is saved under a timestamp prefixed
    UUID name.

    Arguments:
        X_drift: Model input data
        y_drift: Model target data

    Returns:
        Name of the drift set file in the drift bucket.
    '''
    
    create_drift_bucket()

    if y_drift is None:
        df = X_drift
    else:
        df = pd.concat([X_drift, y_drift], axis=1)

    drift_set_name = uuid7str()  # UUID with timestamp
    filename = f"{drift_set_name}.csv"
    
    with BytesIO() as buffer:
        df.to_csv(buffer, index=False)
        buffer.seek(0)
        minio_client.put_object(
            bucket_name=settings.minio_drift_bucket_name,
            object_name=filename,
            data=buffer,
            length=buffer.getbuffer().nbytes,
            content_type="text/csv"
        )
    
    return drift_set_name


def import_drift_data(filename: str) -> pd.DataFrame:
    ''' 
    Download a drift dataset from MinIO and return it as a pandas DataFrame.
    
    Arguments:
        filename: Name of the drift set file (e.g. "abc123.csv")
    
    Returns:
        pd.DataFrame with the drift dataset
    '''
    with minio_client.get_object(
        bucket_name=settings.minio_drift_bucket_name,
        object_name=filename,
    ) as response:
        return pd.read_csv(BytesIO(response.read()))
