import yaml
from networksecurity.exception.exception import custom_exception
from networksecurity.logging.logger import logger
import os, sys
import numpy as np
import pandas as pd
import pickle
from typing import Any
from sklearn.model_selection import GridSearchCV
from sklearn.metrics import r2_score

def read_yaml_file(file_path: str) -> Any:
    try:
        with open(file_path, 'r') as yaml_file:
            return yaml.safe_load(yaml_file)
    except Exception as e:
        raise custom_exception(e, sys) from e

def write_yaml_file(file_path: str, content: Any, replace: bool = False) -> None:
    try:
        if not replace and os.path.exists(file_path):
            raise FileExistsError(f"File already exists: {file_path}")
        
        dir_path = os.path.dirname(file_path)
        if dir_path:
            os.makedirs(dir_path, exist_ok=True)

        with open(file_path, 'w') as yaml_file:
            yaml.dump(content, yaml_file)
            
    except Exception as e:
        raise custom_exception(e, sys) from e

def save_numpy_array_data(file_path: str, array: np.array):
    try:
        dir_path = os.path.dirname(file_path)
        os.makedirs(dir_path, exist_ok=True)
        with open(file_path, 'wb') as file_obj:
            np.save(file_obj, array)
    except Exception as e:
        raise custom_exception(e, sys) from e

def save_object(file_path: str, obj: Any):
    try:
        dir_path = os.path.dirname(file_path)
        os.makedirs(dir_path, exist_ok=True)
        with open(file_path, 'wb') as file_obj:
            pickle.dump(obj, file_obj)
    except Exception as e:
        raise custom_exception(e, sys)
    
def load_object(file_path: str) -> Any:
    try:
        with open(file_path, 'rb') as file_obj:
            return pickle.load(file_obj)
    except Exception as e:
        raise custom_exception(e, sys) from e 

def load_numpy_array_data(file_path: str) -> np.array:
    try:
        with open(file_path, 'rb') as file_obj:
            return np.load(file_obj)
    except Exception as e:
        raise custom_exception(e, sys) from e
    
def evaluate_models(x_train, y_train, x_test, y_test, models, params):
    try:
        report = {}

        for model_name, model in models.items():
            para = params.get(model_name)
            if para is None:
                raise KeyError(
                    f"Missing hyperparameter grid in params for model '{model_name}'."
                )
            

            gs = GridSearchCV(model, para, cv=3)
            gs.fit(x_train, y_train)

            model.set_params(**gs.best_params_)
            model.fit(x_train, y_train)

            y_train_pred = model.predict(x_train)

            y_test_pred = model.predict(x_test)

            train_model_score = r2_score(y_train, y_train_pred)

            test_model_score = r2_score(y_test, y_test_pred)

            report[model_name] = test_model_score

        return report

    except Exception as e:
        raise custom_exception(e, sys)
    

