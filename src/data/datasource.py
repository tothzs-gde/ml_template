import pandas as pd


def from_local_csv(path: str) -> tuple[pd.DataFrame]:
    '''
    '''
    features_to_use = ['Survived', 'Pclass', 'Sex', 'Age', 'SibSp', 'Parch', 'Fare', 'Embarked']
    df_train = pd.read_csv(path, index_col='PassengerId')
    df_train = df_train[features_to_use]
    x_train = df_train.drop(columns='Survived')
    y_train = df_train['Survived']

    return x_train, y_train