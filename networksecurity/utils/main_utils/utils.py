import yaml
from networksecurity.exception.exception import custom_exception
from networksecurity.logging.logger import logger
import os, sys
import numpy as np
import pandas as pd
import pickle
from typing import Any

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
    

    

