import sys
import os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

import numpy as np
import pandas as pd
import yaml

from src.data.drift import detect_drift


def test_detect_drift():
    THRESHOLD = 0.05

    with open("config/data_config.yaml", 'r') as file:
        metadata = yaml.safe_load(file)

    index_columns = metadata['index_columns']

    cols = ['Age', 'SibSp', 'Parch', 'Fare', 'Pclass', 'Sex', 'Embarked']

    reference_df = pd.read_csv('data/titanic.csv', index_col=index_columns)
    reference_df = reference_df[cols]
    
    current_df = pd.read_csv('data/titanic_test.csv', index_col=index_columns)
    current_df = current_df[cols]

    result = detect_drift(
        reference_df,
        current_df,
        threshold=THRESHOLD,
    )

    assert set(result.keys()) == set(cols)
    for col in cols:
        assert result[col]["drift_score"] >= THRESHOLD
        assert result[col]["drifted"] == np.False_
