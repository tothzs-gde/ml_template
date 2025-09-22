import pandas as pd
import yaml
    
from evidently import Dataset
from evidently import DataDefinition
from evidently import Report
from evidently.presets import (
    DataDriftPreset,
    DataSummaryPreset,
)


def check_drift():
    '''
    '''
    with open("config/data_config.yaml", 'r') as file:
        metadata = yaml.safe_load(file)

    cols = metadata['numerical_features'] + metadata['categorical_features']
    schema = DataDefinition(
        numerical_columns=metadata['numerical_features'],
        categorical_columns=metadata['categorical_features'],
    )

    X_ref = Dataset.from_pandas(
        pd.read_csv(
            'data/titanic.csv',
            usecols=cols,
        ),
        data_definition=schema,
    )
    X_sub = Dataset.from_pandas(
        pd.read_csv(
            'data/titanic_test.csv',
            usecols=cols,
        ),
        data_definition=schema,
    )

    report = Report([
        DataDriftPreset(),
        DataSummaryPreset(),
    ])

    my_eval = report.run(X_sub, X_ref)
    
    return my_eval

if __name__ == "__main__":
    check_drift()






# import pandas as pd
# import yaml

# from src.data.drift import detect_drift


# def check_drift():
#     '''
#     '''
#     with open("config/data_config.yaml", 'r') as file:
#         metadata = yaml.safe_load(file)

#     index_columns = metadata['index_columns']
#     target_column = metadata['target_column']

#     cols = ['Age', 'SibSp', 'Parch', 'Fare', 'Pclass', 'Sex', 'Embarked']

#     X_data = pd.read_csv('data/titanic.csv', index_col=index_columns)
#     X_data = X_data[cols]
    
#     X_test = pd.read_csv('data/titanic_test.csv', index_col=index_columns)
#     X_test = X_test[cols]

#     drift_results = detect_drift(
#         reference_df=X_data,
#         current_df=X_test,
#     )

#     return drift_results
