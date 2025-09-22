import re

import pandas as pd
import yaml
from evidently import (
    Dataset,
    DataDefinition,
    Report,
)
from evidently.presets import (
    DataDriftPreset,
)
from scipy.stats import (
    ks_2samp,
    chisquare,
)
from sklearn.preprocessing import OrdinalEncoder


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

    # Align columns
    common_cols = [col for col in reference_df.columns if col in subject_df.columns]
    subject_df = subject_df[common_cols]

    # Encode categorical features
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
