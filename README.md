# ML Template

[General, short description]

## How to run the notebooks

1. Create a virtual environment

```
# Go to the projects root folder

# Create new environment
python -m venv venv

# Activate the new environment
source venv/bin/activate

# Install dependencies
pip install nb_requirements.txt
```

2. Choose the venv for the notebook environment

3. Run the notbooks

## How to deploy the app

Currantly the deployment is only supported through docker-compose / podman-compose.

```
podman-compose up -d
```

## Deployed Services

**App swagger**

Frontend: http://localhost:8000/docs

**MLflow**

Experiment tracking service.

Frontend: http://localhost:8080/

**PostgreSQL**

Database used by MLflow.

**MiniO bucket** (model storage)

S3 cloud storage emulating service. Used to store artifacts such as trained models.

Frontend: http://localhost:9001/

Default credentials:

```
username: minioadmin
password: minioadmin
```

## Project Structure

```
.
├── app.Dockerfile              # Docker image of the src/ application
├── app.env                     # Env vars used by the application at runtime
├── app_requirements.txt
├── data
│   ├── titanic.csv             # Training data
│   └── titanic_test.csv        # Evaluation data
├── docker-compose.yml
├── mlflow-boto3.Dockerfile     # Custom image to enable MLflow to use MiniO as cloud storage
├── nb_requirements.txt         # Dependencies of the notebooks
├── notebooks
│   ├── EDA.ipynb               # Exploratory Data Analysis
│   └── Training Example.ipynb  # PoC training and evaluation of the model
├── README.md
├── src
│   ├── main.py
│   ├── api
│   │   └── api.py              # API endpoint definitions
│   ├── data
│   │   ├── datasource.py       # Local/remote reader functions
│   │   └── pipeline.py         # Data processing pipeline definition
│   ├── model
│   │   ├── evaluate.py         # Evaluation function
│   │   ├── inference.py        # Inference function
│   │   └── train.py            # Training function
│   └── utils
│       ├── logging.py
│       └── settings.py
└── tests
    └── test_main.py
```

## Configuration (env vars)
