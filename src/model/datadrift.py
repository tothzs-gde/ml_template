import pandas as pd
import yaml

from src.data.drift import detect_drift


def check_drift():
    '''
    '''
    with open("config/data_config.yaml", 'r') as file:
        metadata = yaml.safe_load(file)

    cols = metadata['numerical_features'] + metadata['categorical_features']
    X_ref = pd.read_csv(
        'data/titanic.csv',
        usecols=cols,
    )
    X_sub = pd.read_csv(
        'data/titanic_test.csv',
        usecols=cols,
    )

    drift_results = detect_drift(reference_df=X_ref, subject_df=X_sub)
    return drift_results

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
