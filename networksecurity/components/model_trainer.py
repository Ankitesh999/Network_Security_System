import sys, os
import numpy as np
import pandas as pd

from networksecurity.constants import training_pipeline
from networksecurity.entity.artifact_entity import DataTransformationArtifact, ModelTrainerArtifact
from networksecurity.entity.config_entity import ModelTrainerConfig

from networksecurity.utils.ml_utils.model.estimator import NetworkModel
from networksecurity.utils.ml_utils.metric.classification_metric import get_classification_metric
from networksecurity.utils.main_utils.utils import save_object, load_object, load_numpy_array_data, evaluate_models

from networksecurity.logging.logger import logger
from networksecurity.exception.exception import custom_exception

from sklearn.metrics import r2_score
from sklearn.linear_model import LogisticRegression
from sklearn.neighbors import KNeighborsClassifier
from sklearn.tree import DecisionTreeClassifier
from sklearn.ensemble import AdaBoostClassifier, GradientBoostingClassifier, RandomForestClassifier

import mlflow
import dagshub
dagshub.init(repo_owner='Ankitesh999', repo_name='Network_Security_System', mlflow=True)


class ModelTrainer:
    def __init__(self, model_trainer_config: ModelTrainerConfig, data_transformation_artifact: DataTransformationArtifact):
        try:
            self.model_trainer_config = model_trainer_config
            self.data_transformation_artifact = data_transformation_artifact
        except Exception as e:
            raise custom_exception(e, sys)

    def track_mlflow(self, model, metric):
        with mlflow.start_run():
            f1_score = metric.f1_score
            precision_score = metric.precision_score
            recall_score = metric.recall_score
            accuracy_score = metric.accuracy_score

            mlflow.log_params({"f1_score": f1_score,
                               "precision_score": precision_score,
                               "recall_score": recall_score,
                               "accuracy_score": accuracy_score})

            mlflow.sklearn.log_model(model, "model")
        
    def train_model(self, x_train, y_train, x_test, y_test):
        try:
            models = {
                "KNeighborsClassifier": KNeighborsClassifier(),
                "DecisionTreeClassifier": DecisionTreeClassifier(),
                "RandomForestClassifier": RandomForestClassifier(),
                "AdaBoostClassifier": AdaBoostClassifier(),
                "GradientBoostingClassifier": GradientBoostingClassifier(),
                "logistic_regression": LogisticRegression()
            }

            params = {
                "KNeighborsClassifier": {
                    'n_neighbors': [3, 5, 7, 9],
                    #'weights': ['uniform', 'distance'],
                    #'metric': ['minkowski']
                },
                "DecisionTreeClassifier": {
                    #'criterion': ['gini', 'entropy', 'log_loss'],
                    #'splitter': ['best', 'random'],
                    'max_features': ['sqrt', 'log2']
                },
                "RandomForestClassifier": {
                    'criterion': ['gini', 'entropy'],
                    #'max_features': ['sqrt', 'log2', None],
                    #'n_estimators': [8, 16, 32, 64, 128, 256]
                },
                "AdaBoostClassifier": {
                    'learning_rate': [0.1, 0.01, 0.05, 0.001],
                    #'n_estimators': [8, 16, 32, 64, 128, 256]
                },
                "GradientBoostingClassifier": {
                    'learning_rate': [0.1, 0.01, 0.05, 0.001],
                    #'subsample': [0.6, 0.7, 0.8, 0.9, 1.0],
                    #'max_features': ['sqrt', 'log2', None],
                },
                "logistic_regression": {
                    'C': [0.1, 1.0, 10.0],
                    #'solver': ['lbfgs', 'liblinear'],
                    #'max_iter': [100, 200]
                }
            }

            model_report:dict=evaluate_models(x_train=x_train, y_train=y_train, x_test=x_test, y_test=y_test, models=models, params=params)

            best_model_score = max(sorted(model_report.values()))
            
            best_model_name = list(model_report.keys())[list(model_report.values()).index(best_model_score)]

            best_model = models[best_model_name]

            if best_model_score < 0.6:
                raise Exception("No best model found")

            y_train_pred = best_model.predict(x_train)
            classification_train_metric = get_classification_metric(y_true=y_train, y_pred=y_train_pred)
            self.track_mlflow(model=best_model, metric=classification_train_metric)

            y_test_pred = best_model.predict(x_test)
            classification_test_metric = get_classification_metric(y_true=y_test, y_pred=y_test_pred)
            self.track_mlflow(model=best_model, metric=classification_test_metric)

            preprocessor = load_object(self.data_transformation_artifact.transformed_object_file_path)

            model_dir_path = os.path.dirname(self.model_trainer_config.trained_model_file_path)
            os.makedirs(model_dir_path, exist_ok=True)

            network_model =  NetworkModel(preprocessor=preprocessor, model=best_model)

            save_object(self.model_trainer_config.trained_model_file_path, obj=network_model)

            model_trainer_artifact = ModelTrainerArtifact(trainer_model_file_path=self.model_trainer_config.trained_model_file_path,
            train_metric_artifact=classification_train_metric,
            test_metric_artifact=classification_test_metric)

            return model_trainer_artifact

        except Exception as e:
            raise custom_exception(e, sys)
    def initiate_model_trainer(self)->ModelTrainerArtifact:
        try:
            logger.info(f"{'>>'*20}Model Trainer log started.{'<<'*20} ")

            train_file_path = self.data_transformation_artifact.transformed_train_file_path
            test_file_path = self.data_transformation_artifact.transformed_test_file_path

            train_array = load_numpy_array_data(train_file_path)
            test_array = load_numpy_array_data(test_file_path)

            x_train, y_train = train_array[:,:-1], train_array[:,-1]
            x_test, y_test = test_array[:,:-1], test_array[:,-1]

            model_trainer_artifact = self.train_model(x_train=x_train, y_train=y_train, x_test=x_test, y_test=y_test)

            logger.info(f"{'>>'*20}Model Trainer log completed.{'<<'*20} ")

            return model_trainer_artifact

        except Exception as e:
            raise custom_exception(e, sys)



