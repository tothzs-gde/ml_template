# 📘 YAML Configuration Specification for Dynamic ML Pipelines & Hyperparameter Tuning

This documentation defines how to write a YAML configuration file that allows dynamic construction of machine learning pipelines and definition of hyperparameter search spaces. This configuration format is designed to be compatible with tools like `GridSearchCV`.

You can use this file to:

- Define the **structure** of a machine learning pipeline.
- Specify **parameters** for each component.
- Declare **search spaces** for hyperparameter tuning.

---

## Top-Level Structure

The YAML file must define two **top-level sections**:

```yaml
pipeline: <Pipeline definition>
search_parameters: <Hyperparameter search list>
```

## `pipeline` section

Defines the full structure of your ML pipeline, including all preprocessing steps, transformers, feature selectors, classifiers, etc.

### Structure

The pipeline is defined as a recursive structure of objects (classes) with their constructor parameters.

```yaml
class: <full.import.path.to.Class>
params:
  <parameter_1>: <value_1>
  <parameter_2>: <value_2>
  ...
```

### Special Convention: Pipelines and Steps

For components that accept a sequence of named steps (e.g., Pipeline, ColumnTransformer), you must use a steps: or transformers: key inside params, depending on the scikit-learn API.

#### Example: Pipeline step

```yaml
class: sklearn.pipeline.Pipeline
params:
  steps:
    - name: step_name_1
      component:
        class: some.module.TransformerClass
        params: { param1: value, param2: value }

    - name: step_name_2
      component:
        class: some.module.AnotherClass
        params: { ... }
```

#### Example: ColumnTransformer

```yaml
class: sklearn.compose.ColumnTransformer
params:
  transformers:
    - name: num
      transformer:
        class: sklearn.pipeline.Pipeline
        params:
          steps:
            - name: imputer
              component:
                class: sklearn.impute.SimpleImputer
                params:
                  strategy: mean
      columns: [col1, col2, col3]

    - name: cat
      transformer:
        class: sklearn.preprocessing.OneHotEncoder
        params: {}
      columns: [col4, col5]
```

## `search_parameters` section

Defines the hyperparameter grid used for tuning via scikit-learn’s GridSearchCV or similar. This section is a list of dictionaries. Each dictionary represents one or more parameters to vary.

### Format

```yaml
search_parameters:
  - param_name_1: [option1, option2]
  - param_name_2:
      - class: full.import.ClassName
        params:
          some_param: [value1, value2]
```

### How Param Names Work

Use double underscores (`__`) to refer to nested components in the pipeline:

`<step_name_1>__<sub_step>__<param>`

These names must match the step names defined in the `pipeline`.

## Full Schema Specification

| Key | Type | Description
| --- | --- | --- |
| `class`              | `str`        | Full import path to a Python class (e.g., `sklearn.pipeline.Pipeline`) |
| `params`             | `dict`       | Constructor arguments for the class |
| `steps`              | `list`       | (`Pipeline` only) Ordered list of {`name`, `<component>`} dictionaries |
| `transformers`       | `list`       | (Only for `ColumnTransformer`) Each has {`name`, `transformer`, `columns`} |
| `search_paramterers` | `list[dict]` | Hyperparameter search grid; keys match pipeline param paths |