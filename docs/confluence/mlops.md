# MLOps

## Lifecycle

0. Deploy services (MLflow, Postgres, MinIO (or equivalent), Grafana)

1. Exploratory data analysis (EDA)

2. Manually train a model

3. Promote the trained model to `stage: prod`

4. Automated model lifecycle management

    4.1. Inference call

    4.2. Drift detection

    4.3. Trigger model training

    4.4. Promote new model if it is better than the previous

    4.5. Update drift dataset or clean up if new model is worse

### Model evaluation:

- Compare new model to current production on a holdout or recent live dataset
- Use task-specific metrics: e.g., F1 for classification, RMSE for regression
- Optionally: deploy new model in shadow mode and compare predictions before promoting

## Logging

### Request logs

- **timestamp**: When was the request made
- **request_id**: Unique id for the request. Useful to filter logs for the same request.
- **model_version**: Version / tag of the model.
- **task_type**: Classification / Regression / Time series.
- **input_data**: Input features (JSON).
- **model_output**: Raw model predictions.
- **confidence**: Model output confidence if applicable.
- **metadata**: Any other metadata worth logging.

### Strategy

- Batch logging.
- Flush every `N` records or when `flush interval > X seconds`.
- Upload logs to blob storage.
- Use Grafana for monitoring and alerting.

### Format

|   | JSONL | Parquet |
|---|---|---|
| Format type | Text-based, line-delimited JSON | Columnar, binary format |
| Compression | No | Built-in column compression |
| Appendable | Yes, add new lines | No, needs rewriting |
| Readability | Human-readable | Not human-readable, binary format |
| Schema | Flexible | Strict |
| File size | <50MB | 50MB-1GB |

## Drift detection

### Drift logs

**Common**:
- timestamp
- reference_dataset_id
- subject_dataset_id

**Univariate tests** (Evidently):
- feature_name: str
- drifted: bool
- p-value: float
- threshold: float

**Multivariate model-based tests** (Custom):
- drifted: bool
- model_accuracy: float
- threshold: float

### Strategy

- Run both univariate and multivariate model-based tests.
- Run tests in a separate process than the model inference / training
- Use scheduled runs:
    - Every X hour on the last X hour's data.
    - Every hour with a sliding window of X hours.
    - Run once a day.

### Alerting

- Send email / message on drift detection
- Trigger retraining of the model
- Explicitly log drift detection event

## Monitoring

### Service metrics
- Uptime / health check
- CPU usage
- Memory usage
- Disk I/O
- Container health

### API metrics
- Requests per second
- Request count per endpoint
- Response time per endpoint
- Status code breakdown (2xx, 4xx, 5xx)
- 4xx errors
- 5xx errors
- Error rate % over time
- Request origin IP

### Data metrics
- Batch size
- Data quality (missing, invalid values etc.)
- Drift detection

### Model metrics
- Production model version
- Model load time
- Inference time
- Model output distribution
- Prediction confidence
- Drift-triggered retraining event