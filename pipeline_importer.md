# ---
#
# NEEDS UPDATE
#
# ---

# Dynamic Pipeline and Hyperparameter Grid Loader

This Python module provides utilities to dynamically load and instantiate a scikit-learn pipeline and hyperparameter search grid from a single YAML configuration file. The configuration file defines the pipeline architecture and hyperparameter search space, including the full class paths of scikit-learn (or custom) components.

---

## Features

- **Dynamic class import:** Imports any class based on its full Python import path (e.g. `sklearn.pipeline.Pipeline`).
- **Recursive instantiation:** Recursively instantiates nested pipeline components such as steps inside `Pipeline` or transformers inside `ColumnTransformer`.
- **Flexible hyperparameter grid loading:** Converts YAML-defined search parameters into the format required by scikit-learn's hyperparameter tuning tools, instantiating any classes defined within.
- **Single source of truth:** Supports defining both the pipeline structure and hyperparameter tuning parameters in one YAML file.

---

## Functions

### `import_class(class_path: str) -> type`

Imports and returns a class given its fully qualified Python path.

- **Parameters:**
  - `class_path` (`str`): Full import path of the class (e.g. `"sklearn.linear_model.LogisticRegression"`).

- **Returns:**
  - Python class object.

---

### `instantiate_component(component_config: dict) -> Any`

Recursively instantiates a pipeline component from a config dictionary.

- **Parameters:**
  - `component_config` (`dict`): Configuration dictionary with keys:
    - `"class"`: Full class import path.
    - `"params"` (optional): Dictionary of parameters to pass to the class constructor. Nested components can be defined here as well.

- **Returns:**
  - Instantiated object.

---

### `load_config(path: str) -> dict`

Loads a YAML configuration file.

- **Parameters:**
  - `path` (`str`): Path to the YAML config file.

- **Returns:**
  - Parsed configuration dictionary.

---

### `load_pipeline_and_search_params(config_path: str) -> tuple`

Loads and instantiates the pipeline and search parameters from a YAML config file.

- **Parameters:**
  - `config_path` (`str`): Path to the YAML config file.

- **Returns:**
  - Tuple containing:
    - `pipeline`: Instantiated scikit-learn pipeline object.
    - `search_params`: List of hyperparameter dictionaries suitable for grid search.

---

## Usage Example

```python
pipeline, search_params = load_pipeline_and_search_params("config.yaml")

print("Pipeline:")
print(pipeline)

print("\nSearch parameters:")
for param in search_params:
    print(param)
