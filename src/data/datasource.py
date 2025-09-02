import pandas as pd

from src.utils.logging import logger


def from_local_csv(path: str) -> tuple[pd.DataFrame]:
    ''' Imports the .csv file given by the path argument.

    Args:
        path: Path to the .csv file relative to the project's root folder.

    Returns:
        tuple[pd.DataFrame]: Separated input and target dataframes of the 
            imported file.
    '''

    logger.info(f'Importing data from local csv: {path}')

    features_to_use = ['Survived', 'Pclass', 'Sex', 'Age', 'SibSp', 'Parch', 'Fare', 'Embarked']
    df = pd.read_csv(path, index_col='PassengerId')
    df = df[features_to_use]
    x = df.drop(columns='Survived')
    y = df['Survived']

    logger.info(f'Imported dataset {df.shape}')

    return x, y