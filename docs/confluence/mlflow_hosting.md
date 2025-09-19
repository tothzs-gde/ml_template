# MLflow hosting

## Self-hosted

**Pricing**: Infra cost

### Component requirement

MLflow requires *three* main infrastructure components.

1. Tracking server

2. Database

3. Blob storage

The tracking server itself can be hosted on either of the following: **Azure App Service**, **Azure Container Apps**, **Azure Virtual Machines**. This provides the core experiment tracking service and the frontend application.

The database used by MLflow can be either **PostgreSQL** or **Azure SQL Database**. This is where MLflow persists experiments, runs, metrics etc.

For blob storage we can use **Azure Blob Storage**. This is where artifacts and registered models are saved.

## Azure Machine Learning (Managed)

Azure Machine Learning workspaces are MLflow-compatible, which means that you can use an Azure Machine Learning workspace the same way you use an MLflow server. This compatibility has the following advantages:

- Azure Machine Learning doesn't host MLflow server instances, but can use the MLflow APIs directly.

- You can use an Azure Machine Learning workspace as your tracking server for any MLflow code, whether or not it runs in Azure Machine Learning. You only need to configure MLflow to point to the workspace where the tracking should occur.

- You can run any training routine that uses MLflow in Azure Machine Learning without making any changes.

### Model registry in Azure Machine Learning

Azure Machine Learning supports MLflow for model management when connected to a workspace. This approach is a convenient way to support the entire model lifecycle for users familiar with the MLFlow client.

**Pricing**: Pay as you go

**Features**:

- Register, query, load, delete models

- Model versioning, staging, tagging

**Limitations**:

- Azure Machine Learning doesn't support renaming models.

- Machine Learning doesn't support deleting the entire model container.

- Organizational registries aren't supported for model management with MLflow.

- Model deployment from a specific model stage isn't currently supported in Machine Learning.

- Cross-workspace operations aren't currently supported in Machine Learning.

Ref: [Manage models registry in Azure Machine Learning with MLflow](https://learn.microsoft.com/en-us/azure/machine-learning/how-to-manage-models-mlflow?view=azureml-api-2)