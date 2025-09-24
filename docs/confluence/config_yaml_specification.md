# YAML Configuration for ML Pipelines & Hyperparameter Tuning

This documentation defines how to write a YAML configuration file that allows no-code construction of machine learning pipelines and definition of hyperparameter search spaces. This configuration format is designed to be compatible with Scikit-learn's `GridSearchCV`.

You can use this file to:

- Define the **structure** of a machine learning pipeline.
- Specify **parameters** for each component.
- Declare **search spaces** for hyperparameter tuning.

---

## Top-Level Structure

The YAML file can define two **top-level sections**:

```yaml
pipeline: <pipeline definition>
search_parameters: <hyperparameter search list>
```

## `pipeline` section

Defines the full structure of the ML pipeline, including all preprocessing steps, transformers, feature selectors, classifiers, etc.

---

### Structure

The pipeline is defined as a nested tree similarly how a complete sklearn pipeline is represented in text format. Each node must contain at least a `class` key, optionally can define a `params` key, and recommended to have a `name` key, where

- `class` is the complete import path of the component's class.

- `params` is the list of parameters passed to the component's constuctor.

- `name` is a custom name of the component given by the user.

For example:

```yaml
class: sklearn.impute.SimpleImputer
name: imputation_step
params:
  strategy: most_frequent
```

Components can be defined without `params` when they are desired to be instantiated with their default parameters.

```yaml
class: sklearn.dummy.DummyClassifier
```

would be instantiated with it's default parameter values

```python
strategy     = "prior"
random_state = None
constante    = None
```

The `params` are defined as a yaml dictionary as they are requested by the `class`'s constructor.

```yaml
class: sklearn.impute.SimpleImputer
name: imputation_step
params:
  strategy: most_frequent
  fill_value: 0
  copy: false
```

---

### Special components

Components that accept a list of subcomponents in one of their parameters (currently ColumnTransformer and Pipeline are supported) must define these subcomponents in a yaml list.

For example:

```yaml
class: sklearn.pipeline.Pipeline
params:
  steps:
    - name: step_name_1
      class: package.module.class
    - name: step_name_2
      class: package.module.class
```

The `ColumnTransformer` class also requires a list a column names. This list shall be declared inside each list item according to the following example:

```yaml
class: sklearn.compose.ColumnTransformer
params:
  transformers:
    - name: transformer_name_1
      class: package.module.class
      columns: ['a', 'b', 'c']
    - name: transformer_name_2
      class: package.module.class
      columns: ['d', 'e']
```

---

### Complete example pipeline definition

```yaml
pipeline:
  class: sklearn.pipeline.Pipeline
  params:
    steps:
      - name: data_pipe
        class: sklearn.pipeline.Pipeline
        params:
          steps:
            - name: preprocessor
              class: sklearn.compose.ColumnTransformer
              params:
                transformers:
                  - name: num
                    class: sklearn.pipeline.Pipeline
                    columns: ['Age', 'SibSp', 'Parch', 'Fare']
                    params:
                      steps:
                        - name: imputer
                          class: sklearn.impute.SimpleImputer
                          params:
                            strategy: most_frequent
                        - name: scaler
                          class: sklearn.preprocessing.StandardScaler
                  - name: cat
                    class: sklearn.pipeline.Pipeline
                    columns: ['Pclass', 'Sex', 'Embarked']
                    params:
                      steps:
                        - name: imputer
                          class: sklearn.impute.SimpleImputer
                          params:
                            strategy: most_frequent
                        - name: encoder
                          class: sklearn.preprocessing.OneHotEncoder
            - name: feature_selector
              class: sklearn.feature_selection.SelectKBest
              params:
                k: 'all'
      - name: classifier
        class: sklearn.linear_model.LogisticRegression
```

## `search_parameters` section

Defines the hyperparameter grid used for tuning by scikit-learn’s `GridSearchCV`. This section contains a list of dictionaries. Each of these dictionaries define a grid. These dictionaries are made of key-value pairs, where the key is the identifier of a component according to scikit-learn's naming convention, and the value is a list of parameters.

Example based on the pipeline definition above:

```yaml
search_parameters:
  - data_pipe__preprocessor__num__imputer__strategy: ['mean', 'median']
    data_pipe__preprocessor__cat__imputer__strategy: ['most_frequent']
```

Certain components do not only change in parameter values, but in class as well. These different classes are also declared in a list, but they are as a key-value pair, where the key is always **class** and the value is the full import path of the class. The value `null` is also acceptable, if not using this component is also acceptable.

```yaml
search_parameters:
  - data_pipe__preprocessor__num__scaler:
      - null
      - class: sklearn.preprocessing.StandardScaler
      - class: sklearn.preprocessing.MinMaxScaler
```

Classes can be defined similarly as they are defined in the `pipeline` section to specify default parameter values (although it is not recommended in this section).

```yaml
search_parameters:
  - data_pipe__preprocessor__num__scaler:
      - class: sklearn.preprocessing.StandardScaler
        params:
          copy: false
          with_mean: true
          with_std: false
```

It is recommended for clarity to always define the allowed parameters explicitly as different list items according to scikit-learn's naming convention even if only a single value is chosen to be allowed instead of the method described in the `pipeline` section.

```yaml
search_parameters:
  - classifier:
      - class: sklearn.linear_model.LogisticRegression
    classifier__C: [0.1]
    classifier__solver: ['lbfgs', 'liblinear', 'sag', 'saga']
```

Scikit-learn unfortunatelly cannot interpret search grids containing incompatible parameter lists. If you are planning on testing for example multiple classifiers, which do no share the same parameter names, but are instantiated under the same component node in your defined pipeline, then separate search grids need to be defined. This is why the `search_parameters` section is composed of a **list** of yaml dictionaries.

```yaml
search_parameters:
  # Search grid with logistic regression classifier
  - classifier:
      - class: sklearn.linear_model.LogisticRegression
    classifier__C: [0.1]
    classifier__solver: ['lbfgs', 'liblinear', 'sag', 'saga']
  # Search grid with random forest classifier
  - classifier:
      - class: sklearn.ensemble.RandomForestClassifier
    classifier__max_depth: [5, 10, null]
```
