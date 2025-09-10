import pandas as pd
import yaml

from src.utils.logging import logger


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
