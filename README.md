# ML Template

[General, short description]

## How to run

### Full deployment

The following commands clone the project from github, create a virtual environment for the notebooks, and deploys the app and it's related services.

```
git clone git@github.com:tothzs-gde/ml_template.git
cp app.env ml_template/app.env
cp manual.env ml_template/manual.env
cd ml_template
git checkout poc_1
python -m venv venv_nb

source venv_nb/bin/activate
pip install -r nb_requirements.txt
deactivate

podman-compose up --build
```

**App swagger**: http://localhost:8000/docs

**MLflow**: http://localhost:8080/

Experiment tracking service.

**PostgreSQL**:

Database used by MLflow.

**MiniO bucket**: http://localhost:9001/

S3 cloud storage emulating service. Used to store artifacts such as trained models.

Default credentials:

```
username: minioadmin
password: minioadmin
```

The following is a dummy data to test the inference endpoint.

```
# Dummy data to test the inference endpoint
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
```

### Running notebooks

1. Create a virtual environment

```
# Go to the projects root folder

# Create new environment
python -m venv venv_nb

# Activate the new environment
source venv_nb/bin/activate

# Install dependencies
pip install nb_requirements.txt
```

2. Choose the venv for the notebook environment

3. Run the notbooks

## Project Structure

```
.
├── config
│   ├── data_config.yaml            # .
│   ├── pipeline_config_dummy.yaml  # .
│   └── pipeline_config.yaml        # .
├── data
│   ├── titanic.csv                 # Training data
│   └── titanic_test.csv            # Evaluation data
├── docs                            # Code documentation
├── notebooks
│   ├── EDA.ipynb                   # Exploratory Data Analysis
│   └── Training Example.ipynb      # PoC training and evaluation of the model
├── src
│   ├── main.py                     # App entry point
│   ├── api
│   │   ├── models.py               # Api request/response models
│   │   └── api.py                  # API endpoint definitions
│   ├── data
│   │   ├── drift.py                # Data drift detection functions
│   │   └── io.py                   # IO operations
│   ├── model
│   │   ├── datadrift.py            # Data drift detection endpoint logic
│   │   ├── evaluate.py             # Evaluation logic
│   │   ├── inference.py            # Evaluation inference
│   │   ├── pipeline.py             # Pipeline / search grid loader functions
│   │   └── train.py                # Model training logic
│   └── utils
│       ├── logging.py              # Logger settings
│       ├── minio.py                # MinIO bucket creation helper functions
│       └── settings.py             # App settings
├── .dockerignore
├── .gitignore
├── app_requirements.txt
├── app.Dockerfile                  # Docker image of the src/ application
├── app.env.example                 # Env vars used by the application at runtime
├── docker-compose.yml
├── mlflow-boto3.Dockerfile         # Custom image to enable MLflow to use MiniO as cloud storage
├── nb_requirements.txt
├── README.md
└── tests
    └── test_main.py
```

## Configuration (env vars)





Leiras az env varokrol

Solo deployment guide es csatlakozas kulso minio es mlflow servicekhez

Teszteles

Project doksi iras
