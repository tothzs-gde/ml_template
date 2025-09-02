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

## Env vars
