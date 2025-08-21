# DVC

DVC (Data Version Control) is a command-line interface (CLI) tool designed to version control data, models, and machine learning pipelines, while also providing the ability to track experiments. It extends Git by allowing users to version large data files and manage workflows related to machine learning projects. The versioning metadata is stored in the `.dvc` folder within the Git repository, while the actual data files are stored externally (e.g., in cloud storage systems like AWS S3, Google Cloud, or others).

**Homepage**: [https://dvc.org/](https://dvc.org/)

Tags: [data version control], [data pipeline], [ml pipeline], [experiment tracking], [model repository]\_

## Features

### File Version Control

DVC allows for version control of large datasets, models, and other assets like experiments, while keeping Git focused on tracking code. Data is stored externally, while the metadata that tracks the data is stored in your Git repository. DVC can track the exact state of data files, whether that’s datasets, intermediate outputs, or machine learning models, with the ability to revert to any previous version of these files.

### Pipelines

DVC enables the creation and management of reproductible data/ML pipelines. Stages can be defined for each step (1 script one stage) and DVC tracks the dependencies between them. Tracks which datasets and models were used in the pipeline to ensure reproducibility.

### Experiment Tracking

DVC allows you to run, track, and compare multiple experiments easily. You can log parameters, metrics, and outputs and visualize the results over time. Just like datasets, DVC lets you version control machine learning models. This ensures that any model used in a specific experiment can be recreated with the exact same weights and configuration.

### CI Integration

DVC has support for CI tools like GitHub Actions. Could be used to automate data processing, model training and evaluation workflows when a code change occurs.

## Related tools

### VSCode extension

There is a VSCode extension for that gives a GUI for experiment tracking, performance visualization, dashboard to multiple experiments, live tracking of an experiment, and gives a tool for data management over the GUI.

_VSCode Marketplace_: [https://marketplace.visualstudio.com/items?itemName=Iterative.dvc](https://marketplace.visualstudio.com/items?itemName=Iterative.dvc)

<h3 id="dvc-studio">DVC Studio</h3>

This is a web application which seems to be similar in functionality to MLFlow. Free, self-hosted solution. Looks like it covers everything all features of DVC and offers the full functionality of the VSCode extension with the added benefit of online collaboration of team members.

_DVC Studio docs_: [https://dvc.org/doc/studio](https://dvc.org/doc/studio)

### DVCLive

DVCLive is a Python library for logging machine learning metrics and other metadata in simple file formats, which is fully compatible with DVC.

_DVCLive GitHub_: [https://github.com/iterative/dvclive](https://github.com/iterative/dvclive)

### GTO (Git Tag Ops)

GTO (Git Tag Ops) is a tool for creating an artifact registry in your Git repository. Tags can be added to pipelines/models and it manages version numbering and stages like dev, test, prod. Stages can be custom defined.

_GTO docs_: [https://dvc.org/doc/gto](https://dvc.org/doc/gto)

## Interface

- **CLI**: DVC primarily operates via a command-line interface. Common commands include `dvc init`, `dvc add`, `dvc push`, `dvc pull`, `dvc repro`, `dvc run`, and `dvc stage`.
- **Web Interface**: DVC Studio provides a web interface. See [above](#dvc-studio)

## Pricing

The full DVS ecosystem is free and open source for self-hosting.

## Pros

- Supports multiple cloud blob storage providers: S3, MinIO, Azure Blob Storage, Google Cloud Storage, Google Drive, Aliyun OSS
- Using self-hosted storage: SSH & SFTP, HDFS & WebHDFS, HTTP, WebDav
- Support CI/CD tools like Github Actions
- Free and open source
- DVC is mainly a CLI tool, so could be integrated into custom scripts to add some QoL features if needed
- Can read data/models directly from the cloud to memory. No need to store any files locally to access their content.
- Can be used purely for the main feature of data version control, but the supporting tools such as the VSCode extension and DVC Studio are great additions.

## Cons

- Seems like DVC stores each version of the tracked files independently (not tracking incremental changes), therefore duplicating the data on each change. Might be prone to _polluting_ the storage space.
- There is no data access management functionality in DVC. If someone has access to the git repository then they have access to the data.
- DVC extends git's functionality, but it is fully separate when it comes to data storage. There is no pull request feature. Users seem to be able to upload anything without the oversite of git.
- Seems to be focused more on its own ecosystem. There isn't much support to any other tools or services than cloud blob storage providers and CI/CD tools.
- Not a single click/command setup. Might take a some time to set up everything if we use most of the ecosystem.
- Using only the CLI tool, it requires attention and discipline from our team. Probably going to need write a **contribution guide**.
