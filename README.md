# ML Template

[General, short description]

## How to run

### Running notebooks

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

### Full Local Deployment with Podman Compose

Run the following command in the root directory:

```
podman-compose up -d
```

**App swagger**:

Frontend: http://localhost:8000/docs

**MLflow**:

Experiment tracking service.

Frontend: http://localhost:8080/

**PostgreSQL**:

Database used by MLflow.

**MiniO bucket** (model storage)

S3 cloud storage emulating service. Used to store artifacts such as trained models.

Frontend: http://localhost:9001/

Default credentials:

```
username: minioadmin
password: minioadmin
```

### Deploying the app container with remote MLflow and MiniO services

If you have an remotely accessible MLflow and MiniO/AWS S3 service, then you can deploy the app on its own and use the remote services instead of local ones.

Change the following env vars in the app.env file to connect to the correct remote services:

```
# MLflow
MLFLOW_TRACKING_URL=http://mlflow:8080

# MiniO
MINIO_URL=minio:9000
AWS_ACCESS_KEY_ID=minioadmin
AWS_SECRET_ACCESS_KEY=minioadmin
```

Use the following commands in the project's root directory to build and run a podman image:

```
podman build -f app.Dockerfile -t titanic-app-image .

podman run --name titanic_app \
  --env-file ./app.env \
  -p 8000:8000 \
  titanic-app-image
```

### Running the App Locally without Containers

You can also run the code without containerization. To do so follow these steps:

```
# Create new environment
python -m venv venv

# Activate the new environment
source venv/bin/activate

# Install dependencies
pip install app_requirements.txt

# Run the app
python -m src.main
```

## How to run the notebooks

## How to deploy the app

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





Leiras az env varokrol

Solo deployment guide es csatlakozas kulso minio es mlflow servicekhez

Teszteles

Project doksi iras
