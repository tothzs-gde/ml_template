# MLOps

## Request capture

- **timestamp**: When was the request made
- **request_id**: Unique id for the request. Useful to filter logs for the same request.
- **model_version**: Version / tag of the model.
- **task_type**: Classification / Regression / Time series.
- **input_data**: Input features (JSON).
- **model_output**: Raw model predictions.
- **confidence**: Model output confidence if applicable.
- **metadata**: Any other metadata worth logging.

## Logging strategy

- Batch logging.
- Flush every `N` records or when `flush interval > X seconds`
- Upload logs to blob storage
- Use Grafana for monitoring and alerting

## Logging format

|   | JSONL | Parquet |
|---|---|---|
| Format type | Text-based, line-delimited JSON | Columnar, binary format |
| Compression | No | Built-in column compression |
| Appendable | Yes, add new lines | No, needs rewriting |
| Readability | Human-readable | Not human-readable, binary format |
| Schema | Flexible | Strict |
| File size | <50MB | 50MB-1GB |

## Metrics to log

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