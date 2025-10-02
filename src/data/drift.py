import re

import numpy as np
import pandas as pd
import yaml
from evidently import Dataset
from evidently import DataDefinition
from evidently import Report
from evidently.presets import DataDriftPreset
from scipy.stats import ks_2samp
from scipy.stats import chisquare
from sklearn.ensemble import RandomForestClassifier
from sklearn.compose import ColumnTransformer
from sklearn.metrics import accuracy_score
from sklearn.metrics import classification_report
from sklearn.metrics import f1_score
from sklearn.model_selection import train_test_split
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import OrdinalEncoder
from sklearn.preprocessing import OneHotEncoder

from src.utils.logging import logger


def detect_drift(
    reference_df: pd.DataFrame,
    subject_df: pd.DataFrame,
    threshold=0.05,
):
    with open("config/data_config.yaml", 'r') as file:
        metadata = yaml.safe_load(file)

    schema = DataDefinition(
        numerical_columns=metadata['numerical_features'],
        categorical_columns=metadata['categorical_features'],
    )

    X_ref = Dataset.from_pandas(
        reference_df,
        data_definition=schema,
    )
    X_sub = Dataset.from_pandas(
        subject_df,
        data_definition=schema,
    )

    report = Report([
        DataDriftPreset(),
    ])

    evaluation = report.run(X_sub, X_ref)

    drift_results = {}
    for col_eval in evaluation.dict()['metrics']:
        if col_eval['metric_id'].startswith('ValueDrift'):
            drift_results[re.sub(r"[^a-zA-Z0-9_\-.:/ ]+", "", col_eval['metric_id'])] = {
                "drift_score": col_eval['value'],
                "drifted": col_eval['value'] < threshold,
            }
    return drift_results


def detect_drift_manual(
    reference_df: pd.DataFrame,
    subject_df: pd.DataFrame,
    categorical_features=None,
    threshold=0.05,
):
    ''' Univariate drift detection test
    '''
    if categorical_features is None:
        categorical_features = \
            reference_df \
            .select_dtypes(include='object') \
            .columns \
            .tolist()

    numerical_features = [
        col \
        for col in reference_df.columns \
        if col not in categorical_features
    ]

    common_cols = [col for col in reference_df.columns if col in subject_df.columns]
    subject_df = subject_df[common_cols]

    encoder = OrdinalEncoder(handle_unknown="use_encoded_value", unknown_value=-1)
    reference_encoded = reference_df.copy()
    current_encoded = subject_df.copy()
    reference_encoded[categorical_features] = encoder.fit_transform(reference_df[categorical_features])
    current_encoded[categorical_features] = encoder.transform(subject_df[categorical_features])

    drift_results = {}

    for col in common_cols:
        ref_vals = reference_encoded[col].dropna()
        cur_vals = current_encoded[col].dropna()

        if len(cur_vals) == 0:
            drift_results[col] = {"drift_score": None, "drifted": None, "reason": "No current values"}
            continue

        if col in numerical_features:
            # Kolmogorov-Smirnov test
            stat, p_val = ks_2samp(ref_vals, cur_vals)
        else:
            # Chi-squared test
            ref_counts = ref_vals.value_counts().reindex(range(int(ref_vals.max()) + 1), fill_value=0)
            cur_counts = cur_vals.value_counts().reindex(range(int(ref_vals.max()) + 1), fill_value=0)
            
            ref_counts = ref_counts + 1e-6  # prevent zeros
            cur_counts = cur_counts + 1e-6

            # Normalize to same total
            ref_counts = ref_counts / ref_counts.sum()
            cur_counts = cur_counts / cur_counts.sum()

            stat, p_val = chisquare(f_obs=cur_counts, f_exp=ref_counts)

        drift_results[col] = {
            "drift_score": p_val,
            "drifted": p_val < threshold,
        }

    return drift_results


def detect_drift_model_based(
    reference_df: pd.DataFrame,
    subject_df: pd.DataFrame,
    random_state: int | None = None,
    threshold: float = 0.5,
):
    """
    Model based drift detection algorithm. This function trains a Random Forest
    classified model on the mix of two datasets. Data drift is detected based on
    the model's ability to separate the datasets.

    Args:
        reference_df (pd.DataFrame): Drift reference dataset
        subject_df (pd.DataFrame): Test subject dataset
        random_state (int): Seed used when shuffling the two datasets.
    """

    reference_df['DRIFT_TARGET'] = 0
    subject_df['DRIFT_TARGET'] = 1

    shuffled_df = \
        pd.concat([reference_df, subject_df], axis=0) \
        .sample(frac=1, random_state=random_state) \
        .reset_index(drop=True)

    X = shuffled_df.drop('DRIFT_TARGET', axis=1)
    y = shuffled_df['DRIFT_TARGET']

    categorical_cols = X.select_dtypes(include=['object', 'category']).columns.tolist()
    preprocessor = ColumnTransformer(
        transformers=[
            ('cat', OneHotEncoder(handle_unknown='ignore'), categorical_cols)
        ],
        remainder='passthrough'
    )
    pipeline = Pipeline(steps=[
        ('preprocessor', preprocessor),
        ('classifier', RandomForestClassifier(random_state=random_state))
    ])

    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

    pipeline.fit(X_train, y_train)
    y_pred = pipeline.predict(X_test)
    acc = accuracy_score(y_test, y_pred)
    report = classification_report(y_test, y_pred)

    score = np.abs(acc-0.5) * 2
    drifted = score > threshold
    
    log_data = {
        "drift_test": "model-based",
        "drifted": str(drifted),
        "score": score
    }
    logger.info("Model based drift detection completed", extra={"extra_data": log_data})

    print(acc)
    print(report)


if __name__ == "__main__":
    import numpy as np

    SEED = 42
    np.random.seed(SEED)

    N_ROWS = 100
    def gen_random_df(n_rows: int):
        numerical_data = {
            'num1': np.random.rand(n_rows) * 100,
            'num2': np.random.randint(0, 50, n_rows),
            'num3': np.random.normal(0, 1, n_rows)
        }
        categorical_data = {
            'cat1': np.random.choice(['A', 'B', 'C'], n_rows),
            'cat2': np.random.choice(['X', 'Y'], n_rows)
        }
        return pd.DataFrame({**numerical_data, **categorical_data})
    
    ref_df = gen_random_df(N_ROWS)
    sub_df = gen_random_df(N_ROWS)

    detect_drift_model_based(
        reference_df=ref_df,
        subject_df=sub_df,
        random_state=SEED,
    )