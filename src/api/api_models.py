from pydantic import BaseModel
from typing import Any

class InferenceRequest(BaseModel):
    data: list[dict[str, Any]]

    model_config = {
        "json_schema_extra": {
            "examples": [
                {
                    "data": [
                        {
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
                        }
                    ]
                }
            ]
        }
    }
