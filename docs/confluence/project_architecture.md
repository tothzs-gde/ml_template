# Project Architecture

## Core application

The core application is a backend service exposing API endpoints for managing key machine learning workflows, including model training, inference, evaluation, and data drift detection. It serves as the operational backbone for deploying and interacting with machine learning models. Users can manually train models in notebooks, track experiments with MLflow, and register trained models. The service can then retrieve models from the registry to perform tasks such as retraining, model serving, or evaluating performance on test datasets. Additionally, it offers functionality to assess data drift between datasets, supporting robust model monitoring and maintenance.

### API Architecure

The API layer serves as the primary interface to the MLaaS framework, encapsulating the core machine learning operations as RESTful endpoints. Each endpoint corresponds to a specific stage of the ML model lifecycle — training, inference, evaluation, and data drift detection

`POST /train`

The `/train` endpoint handles the retraining of a selected machine learning model. Models are selected by name and version, which can be an integer to choose a specific version, or the word "latest" to choose the last trained model. All trainings results are logged as MLflow runs under the name of `train_{timestamp}`.

**Training steps**:

1. Download input dataset.

2. Split dataset into training and data drift sets.

3. Persist the drift data to a blob storage for later use.

4. Download the selected model.

5. Retrain the downloaded model.

6. Upload the model to the model registry.

7. Add `stage` and `drift-data` tags to the model.

**Necessary improvements**:

- The input dataset and it's data config file is hardcoded into the repository. These shall be removed, and instead downloaded from designated storage location.

**Possible improvements**:

- If no version is selected, then choose the model by the `stage: prod` tag. This would enable automatic retraining of the current model running in producion for example triggerd by the data drift detection algorithm.

- Model testing is not part of the training workflow. A test dataset shall either be downloaded and the new model evaluated on after training, or a part of the training data shall be used for testing (test results would be less comparable in the latter case)

`POST /inference`

The `/inference` endpoint performs predicion using the specified model version on the data sent with the request. Before prediction a data drift detection algorithm runs and logs its results similarly to the `/train` endpoint to MLflow under the name of `infer_{timestamp}`.

The data for the drift detection is automatically fetched from the blob storage. This data had been split from the input dataset of the model training, and the persisted drift data file has been tagged onto the trained model. This tag is retrieved during inference and is used to find the drift data on the blob storage.

**Possible improvements**:

- If no version is selected, then choose the model by the `stage: prod` tag.

- Take an ID with every data point and return the predictions including the corresponding data point ID for easier and more straightforward pairing of the request and reponse at the caller side.

- Decouple the data drift detection algorithm from the inference logic. Including drift detection in the inference endpoint could lead to performance degradation under heavy load.

`POST /evaluate`

The `/evaluate` endpoint enables the evaluation of a selected model on the configured test dataset. Like training and inference, the evaluation step logs results as MLflow runs, named using the previously mentioned timestamp-based convention, `eval_{timestamp}`.

**Possible improvements**:

- The test dataset is currently hard coded into the algorithm. This dataset shall be uploaded to a central data storage and downloaded from there instead of using the file currently in the repository.

`POST /data-drift`

The `/data-drift` endpoint performs statistical comparison between two datasets.

**Possible improvements**:

- Currently both the reference dataset and the subject dataset is hard coded into this endpoint. The drift detection logic itself however is working with parameters supplied during the inference call. This endpoint would provide further ability to check either manually or by external systems the drift between two datasets. The endpoint parameters shall be updated according to these needs.

`POST /health`

A simple health check endpoint that returns `200 OK` if the service is live. This is used for orchestration, container health monitoring, and deployment readiness checks.

## MLflow (dependency)

MLflow is a lightweight platform for managing machine learning workflows, with a focus on experiment tracking and model lifecycle management. In our setup, we use MLflow to organize projects as experiments, where each model training, evaluation, or inference task is logged as a run. This allows us to track training and validation metrics, hyperparameters, and outputs in a structured way, whether models are trained manually or through automated pipelines. MLflow also stores artifacts like models and drift reports, and provides a registry for managing model versions and stages. While MLflow handles the orchestration, it relies on external storage (e.g. Azure Blob Storage) to store artifacts and registry content.

## Blob Storage (dependency)

The system uses MinIO, an S3-compatible object storage service, as the default backend for storing model artifacts, drift datasets, and other files required during the machine learning lifecycle. MinIO is deployed as part of the local development environment via Docker Compose, making it easy to run the full stack locally or in self-hosted environments.

Blob storage is used in two main contexts:

1. **Model registry and artifact store** – MLflow relies on S3-compatible storage to persist model files, training metrics, and other logged artifacts.

2. **Data drift datasets** – During model training, a portion of the input data is saved separately as a drift baseline sample. These samples are stored in blob storage and linked to the corresponding model version via a custom drift-data tag in the MLflow model registry. This setup allows automated retrieval during inference or drift checks.

While MinIO is the default option, the system is designed to be cloud-agnostic. Any S3-compatible or blob storage system (e.g., Azure Blob Storage, AWS S3, Google Cloud Storage) can be used with minor configuration and code changes.