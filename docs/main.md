# ML template

## API Overview

In this section we discuss the the high level concepts of the service through the public inteface provided by the API and the questions that arise related to them.

### POST /train

The /train API endpoint is responsible for training new models. Training requires data, which could be passed to the training algorithm in several ways. The simples form is directly passing it to the endpoint. A portion of the training dataset needs to be set aside for later use in the data drift checking algorithm. The new model can be trained with MLflow autologging enabled to persist training information, metrics and any other useful information. MLflow runs are named "*train_{datetime}*".

On successful training the endpoint shall return the run_name, registered_model_name, model_version and a {status: success} message. Runtime errors might occure, in which case a {status: failed} message is enough. The MLflow frontend doesn't allow inspection of errors in failed runs, so the most informative source of the failure is the logs themselves.

#### Data fetching

Passing a large training dataset is not the most efficient solution. Better solutions are tightly coupled with the actual data storage solution though, so **this will need customization for each project**.

#### Data drift sample storig

The need for storing a separate data sample complicates the solution. There is a MinIO S3 storage already available in the docker-compose file. We can store the data sample there to eliminate the need for manually passing it to the data drift algorithm for now. In theory the project allows deployment of multiple models and also training new models in parallel. This means multiple drift samples coexisting at any given time. These samples need to be identifiable to be used where they are needed.

The drift sample is a subset of a dataset of which the rest of the data points are part of the training set. This training set is used to train the, let's say, current production model. This means that the drift sample is indirectly tied to the model through it's superset. At a later point of the model's lifecycle when either the inference or evaluation endpoints are called, the model is pulled through MLflow from the repositiory. This means that if we **tag** the the model with a **drift sample ID**, then we can also fetch the exact drift sample from the MinIO storage. *Migrating to a different storage method would require a different solution to this drift sample versioning problem.*

### POST /inference

The /inference API endpoint is responsible for predicting the output for a given input. Similarly to the /train endpoint, the direct data passing is the most convenient at the moment. As long as the calls contain a single data point or the calls to this endpoint are frequent enough to keep the sent data small, this solution could be useable later on. A different solution would be to give some IDs, datetime ranges or use a different method to identify the inference input data inside a database for example. This endpoint depends on the data drift checking function and needs to store the input-prediction pairs. MLflow runs are named "*infer_{datetime}*".

#### Storing the input-prediction pairs

Once again the simultaniously running models are affecting the decisions here. One approach is storing all predictions together. This is achievable by adding a extra column for example to the data point which stores the model's name and version. Another option would be to store this data per model name+version or per model instance. The last solution eliminates potention issues emerging from multiple models trying to access the same resource, but would produce the least manageable storage system.

### POST /evaluate

The /evaluate API endpoint allows the user to evaluate a model's performance on a given dataset. It only open issue of this endpoint is the data fetching as it is for the /train endpoint. MLflow runs are named "*eval_{datetime}*".

### POST /data-drift

This endpoint offers two interfaces. The endpoint itself is for the user to manually initiate a data drift check, while the underlying function is imported and used by the /inference endpoint. It either has one or two datasets as inputs. The first one is mandatory, it is the subject of the test. The second one is optional. If not provided then the current baseline, i.e., the current production model's tagged and stored drift sample shall be used, otherwise the provided data shall be the baseline.

MLflow directly doesn't support data drift checking, but we could still log these tests in runs for example under the name of "*drift_{model_name}_{model_version}_{datetime}*" for example to log drift events only. In this case the subject data could be saved also for later analysis?

Later on the output of this endpoint shall be connected to Grafana or similar service to track and alert. Based on specified conditions a new model training could also be triggered.

### GET /health

This is a healthcheck endpoint. It's only purpose is to return a HTTP 200 response if the service is available. Going to be used for service monitoring.