from sklearn.compose import ColumnTransformer
from sklearn.discriminant_analysis import StandardScaler
from sklearn.feature_selection import SelectKBest
from sklearn.impute import SimpleImputer
from sklearn.linear_model import LogisticRegression
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import OneHotEncoder


def get_pipeline():
    '''
    '''
    numeric_features: list[str] = ['Age', 'SibSp', 'Parch', 'Fare']
    categorical_features: list[str] = ['Pclass', 'Sex', 'Embarked']


    numeric_transformer = Pipeline(steps=[
        ('imputer', SimpleImputer(strategy='most_frequent')),
        ('scaler', StandardScaler()),
    ])

    categorical_transformer = Pipeline(steps=[
        ('encoder', OneHotEncoder()),
        ('imputer', SimpleImputer(strategy='most_frequent')),
    ])

    preprocessor = ColumnTransformer(
        transformers=[
            ('num', numeric_transformer, numeric_features),
            ('cat', categorical_transformer, categorical_features)
        ])
    feature_selector = SelectKBest(k='all')

    data_pipe = Pipeline(steps=[
        ('preprocessor', preprocessor),
        ('feature_selector', feature_selector),
    ])

    pipeline = Pipeline(steps=[
        ('data_pipe', data_pipe),
        ('classifier', LogisticRegression(C=1, solver="lbfgs", max_iter=1000))
    ])

    return pipeline