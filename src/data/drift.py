import pandas as pd
from scipy.stats import ks_2samp, chisquare
from sklearn.preprocessing import OrdinalEncoder

def detect_drift(
    reference_df: pd.DataFrame,
    current_df: pd.DataFrame,
    categorical_features=None,
    threshold=0.05
):
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
    common_cols = [col for col in reference_df.columns if col in current_df.columns]
    current_df = current_df[common_cols]

    # Encode categorical features
    encoder = OrdinalEncoder(handle_unknown="use_encoded_value", unknown_value=-1)
    reference_encoded = reference_df.copy()
    current_encoded = current_df.copy()
    reference_encoded[categorical_features] = encoder.fit_transform(reference_df[categorical_features])
    current_encoded[categorical_features] = encoder.transform(current_df[categorical_features])

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
