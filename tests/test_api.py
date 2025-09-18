import sys
import os
from unittest.mock import patch
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))


from fastapi.testclient import TestClient

from src.main import app


client = TestClient(
    app,
    base_url="http://test_url.hu",
)


@patch("src.api.api.train")
def test_train(mock_train):
    mock_train.return_value = ("run_123", "new_model", "v3")

    response = client.post("/train")

    assert response.status_code == 200
    assert response.json() == {
        "run_name": "run_123",
        "registered_model_name": "new_model",
        "registered_model_version": "v3",
        "status": "success",
    }


@patch("src.api.api.infer")
def test_inference_error(mock_infer):
    mock_infer.return_value = (1)

    request_data = {
        "data": [{
            "Name": "Hello World",
            "Ticket": "No.2356",
            "Cabin": "front left",
            "Pclass": 1,
            "Sex": "male",
            "Age": 21,
            "SibSp": 1,
            "Parch": 1,
            "Fare": 40.5,
            "Embarked": "S"
        }]
    }
    
    response = client.post("/inference", json=request_data)

    assert response.status_code == 200
    assert response.json() == {"status": "success", "prediction": 1}


@patch("src.api.api.evaluate")
def test_evaluate_error(mock_evaluate):
    mock_evaluate.return_value = (0.89)

    response = client.post("/evaluate")

    assert response.status_code == 200
    assert response.json() == {"status": "success", "accuracy_score": 0.89}


@patch("src.api.api.check_drift")
def test_drift_error(mock_check_drift):
    mock_check_drift.return_value = ({
        "Age": {
            "drift_score": 0.7023427077378919,
            "drifted": "False"
        },
        "SibSp": {
            "drift_score": 0.9905968490976704,
            "drifted": "False"
        },
        "Parch": {
            "drift_score": 0.9999999704869827,
            "drifted": "False"
        },
        "Fare": {
            "drift_score": 0.7512564942991772,
            "drifted": "False"
        },
        "Pclass": {
            "drift_score": 0.9571654941014089,
            "drifted": "False"
        },
        "Sex": {
            "drift_score": 0.9812566422871262,
            "drifted": "False"
        },
        "Embarked": {
            "drift_score": 0.9846816839996834,
            "drifted": "False"
        }
    })

    response = client.post("/drift")

    assert response.status_code == 200
    assert response.json() == {
        "status": "success",
        "drift_results": {
            "Age": {
                "drift_score": 0.7023427077378919,
                "drifted": "False"
            },
            "SibSp": {
                "drift_score": 0.9905968490976704,
                "drifted": "False"
            },
            "Parch": {
                "drift_score": 0.9999999704869827,
                "drifted": "False"
            },
            "Fare": {
                "drift_score": 0.7512564942991772,
                "drifted": "False"
            },
            "Pclass": {
                "drift_score": 0.9571654941014089,
                "drifted": "False"
            },
            "Sex": {
                "drift_score": 0.9812566422871262,
                "drifted": "False"
            },
            "Embarked": {
                "drift_score": 0.9846816839996834,
                "drifted": "False"
            }
        }
    }
