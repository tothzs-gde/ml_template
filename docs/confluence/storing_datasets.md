# Storing datasets

## Key requirements & constraints

Typical requirements that influence the choice:

- **Scalability**: ability to store large volumes of data (raw, intermediate, features, drift sets, etc.).

- **Versioning / lineage / reproducibility**: need to record which exact dataset version (or partition) was used for a training run, drift detection, etc.

- **Access patterns**: sometimes bulk streaming reads (e.g. training), sometimes random access (e.g. feature lookup, drift scoring).

- **Latency / throughput**: production inference or drift detection, may require fast access.

- **Metadata / indexing / search**: ability to query datasets (versions, schemas, statistics) by metadata, tags, and so on.

- **Cost and efficiency**: storage cost (cold vs hot), duplication, incremental updates vs full snapshots.

- **Security, governance, and retention policies**: auditability, access control, regulatory compliance.

## 1. Store datasets (or partitions thereof) as artifacts in MLflow (or other experiment tracking)

### Description

MLflow (and similar systems such as Weights & Biases artifacts, Comet, etc.) allows the logging of artifacts alongside runs. In MLflow, artifact stores are separate from the “backend store” (which holds parameters, metrics, tags). The artifact store can be configured to point to a blob storage, file system, S3, GCS, etc.

In this scheme, each experiment run could log:

- The exact training dataset used for the run (e.g. a Parquet / CSV / HDF5 / TFRecord file)
- The test / validation split
- The drift reference set used
- Preprocessed / featurized versions
- Any data slices or subsamples used

Then, when you later inspect a run, you know precisely which dataset artifact was tied to that run.

###### Some teams even bake custom “dataset-flavors” so that datasets are treated as first-class tracked artifacts in MLflow (or attach dataset version IDs as tags).

### Pros

- **Tight association with the experiment**: it’s very clear which dataset version was used in that run.
- **Reproducibility**: you can always re-download exactly the same artifact.
- **Compatibility**: MLflow supports many artifact backends (S3, Azure Blob, GCS, HDFS, NFS, SFTP) 
- **Simplicity for small to medium scale**: for moderate dataset sizes, logging them is straightforward.
- **Central UI / lineage view**: you can see artifacts per run in the same tool you inspect metrics, hyperparameters, etc.

### Cons

- **Size / scalability constraints**: if your training or drift datasets are very large (hundreds of GBs, TBs), logging them as artifacts can become impractical—upload times, storage cost, or serving costs may be high.
- **Duplication / inefficiency**: multiple runs may re-log largely overlapping datasets, causing duplication.
- **Not optimized for fine-grained updates or deltas**: artifact systems treat artifacts as “blobs”, not incremental diffs or granular versioned rows.
- **Limited queryability**: you can’t easily query “all dataset versions with X schema change” or run fast SQL-like scans over all versions.
- **Potential coupling / tool lock-in**: you may tie dataset storage logic to your experiment tracking tool.

### Real‑world examples / notes:

- The MLflow documentation explicitly supports storing arbitrary data files / datasets as run artifacts, though it cautions about large artifact sizes.
- In their “Tracking Image Datasets” example, MLflow logs the image splits (train/val/test) as artifacts.

In many industrial settings, teams use this scheme for smaller (or sampled) datasets, but not for full-scale data.

## 2. Use a blob / object storage + versioning / convention (S3, Azure Blob, GCS, HDFS, MinIO, etc.)

### Description

Here the main dataset files (raw data, preprocessed, drift windows, features) are stored in a scalable blob / object store. Versioning is managed either via:

- Naming / directory conventions (e.g. `dataset_name/v1/`, `dataset_name/v2/`)
- Including date or timestamp partitions (e.g. `dataset_name/2025-09-25/…`)
- Using object store versioning features (e.g. S3 versioning, blob storage snapshots) where the storage system tracks object versions
- Layering a versioning or manifest metadata system on top (e.g. DVC, Delta Lake, Apache Iceberg, Apache Hudi, or custom)

Then your pipelines / experiment tracking refer to a particular version in the blob store.

For example:

- Training uses `s3://my-bucket/datasets/training/v3/part-*.parquet`
- Drift detection uses `s3://my-bucket/datasets/drift-reference/v2/`
- In addition, a “latest” alias might point to the most recent version, or metadata store holds pointers to current version.

Often, this blob store acts as the “source of truth” for datasets, with downstream jobs reading from it.

Many guidelines from cloud providers recommend object storage as the backbone of ML data storage (e.g. Google’s [Design storage for AI/ML workloads](https://cloud.google.com/architecture/ai-ml/storage-for-ai-ml#archive-tab)).

### Pros

- **Scalability & cost-effectiveness**: object storage is horizontally scalable and relatively low cost (especially for cold or infrequently accessed versions).
- **Decoupling from compute and experiment tooling**: the dataset store is independent and can serve multiple consumers.
- **Flexibility**: you can use any file format (Parquet, Avro, TFRecords, CSV, etc.), partitioned layouts, and apply lifecycle or archival policies.
- **Mature ecosystem support**: many tools (Spark, TensorFlow, PyTorch, Dask, etc.) can read directly from blob storage.
- **Versioning + deduplication with external layer**: when paired with versioning frameworks (see below), you can avoid duplication.

### Cons

- **Manual bookkeeping**: you must maintain consistent naming / version pointers or a manifest catalog to know which version was used.
- **Metadata / search limitations**: unless you build or use a metadata catalog (e.g. a dataset registry), you can’t easily query dataset versions by schema, lineage, tags, etc.
- **Access latency / throughput constraints**: random small reads (point lookup) may be inefficient compared to databases or caching layers.
- **Lack of strong ACID / update semantics**: object storage is immutable (or append-only) in many cases; updates or deletes are generally handled via rewriting objects rather than in-place edits.
- **Versioning via object store is coarse-grained**: S3 versioning is per-object; it doesn’t understand higher-level dataset structure.

### Variants / enhancements:

- Use **Delta Lake**, **Apache Iceberg**, or **Apache Hudi** layered on top of object storage. These systems bring transactional table semantics (ACID operations, schema evolution, time travel) to data in object stores.
- Use **content-addressable storage** / **hash-based deduplication**: e.g. a tool like DVC (see below) stores blobs in object storage keyed by content hash, avoiding duplicate storage.

### Real-world references:

- Google’s “[Design storage for AI/ML workloads](https://cloud.google.com/architecture/ai-ml/storage-for-ai-ml#archive-tab)” recommends using managed file systems or blob storage (e.g. Cloud Storage) for dataset storage, and lifecycle management for archival.
- Many public “best practices for versioning data / models” guides use blob storage as the default “remote storage” backend (for example DVC’s documentation)

In practice, for large scale “production” datasets, the blob + versioning approach seems to be the standard.

## 3. Use a NoSQL / document / key‑value store for datasets or partitions

### Description

In this approach, you store data (or parts of it) in a NoSQL system (e.g. document store like MongoDB, key-value stores, Cassandra, or a wide-column store). You might, for example:

- Store each “data point” or record with fields, and perhaps metadata indicating which dataset split (training / drift / test) it belongs to.
- Keep multiple versions by appending version tags to each record (e.g. version = v1, v2).
- Use the store for fast incremental access, filtering, or slice-based retrieval.

This is more common in scenarios where data is relatively small or semi-structured, or where you need point lookups / queries.

### Pros

- **Fine-grained updates**: you can update or insert records incrementally (e.g. drift windows, labeling corrections).
- **Queryability / indexing**: NoSQL stores support fast queries, filters, indexing on fields, so you can efficiently retrieve subsets.
- **Low-latency / real-time**: for small-scale inference or drift detection, NoSQL stores can provide quick access to individual records.
- **Schema flexibility**: document-style stores can evolve schemas more flexibly than relational systems.

### Cons

- **Scalability & cost**: NoSQL stores are not optimized for massive bulk storage of large tables / high-dimensional data; storing TBs of features might be expensive or slow.
- **Duplication / inefficiency for large features**: storing feature vectors or large arrays inside NoSQL may bloat storage and performance.
- **Versioning complexity**: versioned record-level changes may require custom patterns (e.g. snapshot tables, version tags).
- **Not ideal for sequential / batch processing**: bulk reads might be slower or less efficient than optimized blob storage or columnar formats.
- **Operational complexity**: scaling NoSQL for analytics workloads may require expertise (sharding, compaction, indexing).

## 4. Use a relational (SQL) database / data warehouse

### Description

In this approach, structured datasets (tables) are stored in an RDBMS (e.g. PostgreSQL) or data warehouse (e.g. BigQuery).

- Store all raw or preprocessed data in tables, possibly partitioned by date or version.
- Add a column (or set of columns) indicating dataset version / split (training / drift / test).
- Use SQL queries or views to select the appropriate partitioned datasets.
- Use database features such as time‑travel or snapshotting (if supported) to retrieve historical versions.

Alternatively, one might leave the historical raw data elsewhere (e.g. in blob storage) and only load subsets into the database for analysis / serving.

### Pros

- **Strong query capabilities**: you can express complex joins, filters, aggregations, slicing — which is useful for drift detection, feature engineering, etc.
- **Transactionality, constraints, ACID semantics**: consistency guarantees benefit data integrity.
- **Incremental updates**: easy to insert, update, delete rows, and maintain incremental drift windows.
- **Unified view**: schema and data definitions are explicit, which helps with governance and team collaboration.

### Cons

- **Scalability limitations**: relational systems struggle to scale to truly large datasets (hundreds of millions or billions of rows), especially for heavy ML use patterns.
- **Performance for bulk training**: pulling large volumes of data from SQL for training may become a bottleneck.
- **Versioning overhead**: versioning fine-grained (row-level) history or branching is non-trivial.
- **Duplication / storage cost**: storing multiple versions may cause data bloat or require complex pruning / archival.
- **Schema rigidity**: evolving feature schemas may require migrations or alter-table operations.

### Real-world examples / references:

- Some teams use Snowflake or BigQuery as their “single source of truth” ledger for tabular data, then extract snapshots for ML pipelines. But reproducibility (tracking which snapshot was used) becomes a challenge. For instance, practitioners using Snowflake note that its built-in “time travel” window (e.g. 90 days) may not suffice for long-term ML versioning across years.
- In hybrid settings, teams often extract subsets of SQL/warehouse data (e.g. `SELECT * FROM table WHERE date < X`) and export them into more ML-friendly formats for training, rather than training directly from SQL.

In sum, SQL/warehouses are often used for upstream data engineering, but not typically as the primary training or drift-dataset store in large-scale ML systems.

## 5. Embed “dataset membership” or version tags inside the data itself (a column or label)

### Description

Under this pattern, you store all raw or unified data in a single large data source (blob, database, warehouse, etc.), but include a column (e.g. `split_type`, `version_id`, `dataset_tag`) indicating whether a given data point belongs to the “training set”, “validation set”, “drift reference window”, etc.

Then the pipelines / model code simply filter on that column to pick the correct points. As new data comes in, new “version_id” values are assigned, and retraining or drift detection logic uses filtering.

Alternatively, you might maintain separate “dataset assignment” tables (mapping record IDs to version groups), but the idea is logically similar.

### Pros

- **Simplicity**: you don’t need to physically duplicate data into multiple folders or tables for splits; the splitting logic is implicit and queryable.
- **Ease of incremental updates**: new data can be appended with new version_id without duplicating old ones.
- **Queryability and lineage**: you can see in one unified table which data points belong to which version or split.
- **Data integrity / single source of truth**: reduces duplication or divergence between versions.

### Cons

- **Large-scale pipeline coupling**: filtering logic is everywhere; you must be very careful about “leakage” or accidentally mixing splits.
- **Versioning complexity**: if you want to treat “dataset version v1” as immutable and then branch to “v2”, you need to ensure historical version records aren’t altered, and new versions are clearly distinguished.
- **Limited historical immutability**: unless you make full snapshots or explicitly enforce immutability, historical splits might get overwritten.
- **Harder retroactive replay**: if you later decide to change the split logic or resample, retroactively changing the membership is tricky without recomputing and potentially rewriting large data.

## 6. Use dedicated dataset / feature stores / catalogs (hybrid systems)

### Description

Many modern ML systems adopt a feature store or data catalog / dataset registry that provides:

- A central repository for features or datasets, often with versioning, lineage, and access APIs.
- Hybrid backing storage (blob storage, databases, caches) but with a unified interface.
- Ability to serve features to production inference, as well as to training pipelines.
- Metadata management: schema, version, tags, freshness, data quality, statistics.

In effect, these systems decouple the raw storage medium from the logical dataset abstraction.

In some more general systems, the concept of a Model Lake or Model / Dataset Lake is emerging — i.e. a unified repository for datasets, models, code, metadata, versioning, and governance. A recent paper “[Model Lake](https://arxiv.org/html/2403.02327v2)” proposes such architecture.

### Pros

- **Separation of concerns**: experiment tracking, dataset versioning, feature serving are decoupled.
- **Rich metadata and lineage**: you can query dataset versions, transformations applied, who authored them, and which model runs used them.
- **Optimized storage & caching**: the system can automatically manage tiering, caching, or partitioning behind the scenes.
- **Interoperability & reuse**: multiple models or teams can reuse the same feature / dataset definitions.
- **Production inference support**: feature stores often provide low-latency serving APIs, which is complementary to dataset storage.

### Cons

- **Operational complexity**: you must run, maintain, evolve the feature store / catalog infrastructure.
- **Learning curve / tooling lock-in**: adopting a full feature store often requires new APIs and conventions.
- **Cost and performance tuning**: for extremely high throughput or large datasets, the abstraction may introduce overhead.
- **Not all datasets are “features”**: for experimental splits, full raw inputs, or huge data archives, you may still need lower-level blob storage beneath.

### Examples / references:

- Many enterprises use feature stores to serve inference features, and reuse the same feature pipelines in training (ensuring consistency). (E.g. Feast, Tecton, internal in-house solutions.)
- The “Model Lake” concept suggests unifying datasets, models, metadata, versioning in a governance-first architecture.

In practice, a hybrid architecture is common: raw data lives in blob storage, but the feature store sits on top as the curated interface, and experiment tracking refers to dataset / feature-store versions.

## Hybrid / Multi-tier architectures

In real enterprise ML systems, you often see hybrid architectures combining multiple of the above strategies, e.g.:

1. **Blob storage / object store** is the long-term ground truth of raw and processed datasets, with versioning via directories or delta layers (Iceberg, Hudi).

2. **Feature store** or **dataset registry** sits above that to provide curated interfaces, versioning, and lineage APIs.

3. **Experiment tracking (MLflow, W&B, etc.)** logs references (URIs, version IDs), small sampled dataset artifacts, and tie-in of dataset → model → metrics.

4. **Online / low-latency stores** (NoSQL, in-memory caches) host the features needed for inference or drift detection in real time.

5. **Archive / snapshot storage** holds older versions for compliance purposes.
