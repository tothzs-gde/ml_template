# How to store data

|||||
|---|---|---|---|
| Data type | Input | Ground truth | Prediction |
| When available | At inference | X days after inference | At inference |
| Source | Request data | ??? | Model output |
| Storage location | (blob) data/x | (blob) data/y_true | (blob) data/y_pred |
| Naming | [epochtime].parquet | [epochtime].parquet | [epochtime].parquet |

## Open questions

- How frequent are the inference requests?
- What is the average batch size per inference request?
- Should we store each request in separate files, or should we aggregate them?
- How do we manage data aggregation? (Scheduled daily process?)
- When will ground truth data be available?
- How do we receive groud truth data?
- Do individual data points have an ID? If not, how do we match the stored inputs with the ground truth?

# Logging

1. Runtime logs > `.jsonl` files > Promtail > Loki > Grafana
2. Data logs (input data, model output) > `.parquet` > Data registry

- Should we handle drift detection logs as 'Runtime logs' or do we handle them as 'Data logs'?
- Promtail requires some persistent storage. Mainly to track which logs has been sent I think.
- Loki needs proper persistent volume attached. It is the database that stores the logs.
- Grafana probably uses some storage to save configurations

# How do we schedule drift detection?

1. At every inference call -> Frequent inference calls with small batch size might not provide enough data to have reliable drift results -> Collect past X number of exported input data + current call's data to run drift detection

2. Scheduled every X hours / daily -> Run drift detection independently -> collect data as in `1.` or use data since last run

- When do we trigger automatic model retraining?
    
    1. At every drift trigger
    2. After N consecutive triggers
    3. After N out of M calls detected drift
    4. Daily / Weekly regardless of drift detection (Depends on how frequestly we get fresh ground truth data)
