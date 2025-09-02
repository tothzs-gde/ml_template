import mlflow
from mlflow.models import infer_signature
from sklearn.discriminant_analysis import StandardScaler
from sklearn.model_selection import GridSearchCV
from sklearn.model_selection import StratifiedKFold
from sklearn.preprocessing import MinMaxScaler

from src.data.datasource import from_local_csv
from src.data.pipeline import get_pipeline
from src.utils.logging import logger
from src.utils.settings import settings


def train():
    ''' 
    '''

    # TEST GRID
    # param_grid = {
    #     'data_pipe__preprocessor__num__imputer__strategy': ['mean'],
    #     'data_pipe__preprocessor__num__scaler': [MinMaxScaler()],
    #     'data_pipe__preprocessor__cat__imputer__strategy': ['mean'],
    #     'data_pipe__feature_selector__k': [1],
    #     'classifier__C': [1],
    #     'classifier__solver': ['lbfgs'],
    # }

    param_grid = {
        'data_pipe__preprocessor__num__imputer__strategy': ['mean', 'median', 'most_frequent', 'constant'],
        'data_pipe__preprocessor__num__scaler': [MinMaxScaler(), StandardScaler()],
        'data_pipe__preprocessor__cat__imputer__strategy': ['mean', 'median', 'most_frequent', 'constant'],
        'data_pipe__feature_selector__k': list(range(1, 8)),
        'classifier__C': [0.1, 1, 10],
        'classifier__solver': ['lbfgs', 'liblinear', 'sag', 'saga'],
    }

    logger.info('importing train data')
    x_train, y_train = from_local_csv('data/titanic.csv')

    logger.info('assembling pipeline')
    pipeline = get_pipeline()

    logger.info('fitting model')
    skf = StratifiedKFold(n_splits=5, shuffle=True)
    grid_search = GridSearchCV(estimator=pipeline, param_grid=param_grid, scoring="accuracy", cv=skf, verbose=1)
    grid_search.fit(x_train, y_train)

    best_model = grid_search.best_estimator_
    training_accuracy = grid_search.best_score_

    logger.info('evaluating model')
    x_test, y_test = from_local_csv('data/titanic_test.csv')
    test_accuracy = best_model.score(x_test, y_test)

    logger.info('mlflow tracking')
    mlflow.set_tracking_uri(uri=settings.mlflow_tracking_url)
    mlflow.set_experiment(experiment_name=settings.mlflow_experiment_name)

    with mlflow.start_run():
        mlflow.log_params(best_model.get_params())
        mlflow.log_metric("training_accuracy", training_accuracy)
        mlflow.log_metric("test_accuracy", test_accuracy)

        logger.info('infering sign')
        signature = infer_signature(x_train, best_model.predict(x_train))

        logger.info('logging model')
        model_info = mlflow.sklearn.log_model(
            sk_model=best_model,
            name=settings.mlflow_model_name,
            signature=signature,
            input_example=x_train.head(),
            registered_model_name=settings.mlflow_registered_model_name,
        )
