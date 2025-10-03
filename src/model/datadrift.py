import pandas as pd
import yaml

from src.data.drift import detect_drift
from src.data.drift import detect_drift_model_based
from src.data.quality import check_data_quality


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

    check_data_quality(df=pd.DataFrame(X_sub),)
    drift_results = detect_drift(reference_df=X_ref, subject_df=X_sub)
    detect_drift_model_based(reference_df=X_ref, subject_df=X_sub)
    return drift_results

if __name__ == "__main__":
    check_drift()
