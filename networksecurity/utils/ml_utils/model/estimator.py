import os, sys
from networksecurity.logging.logger import logger
from networksecurity.exception.exception import custom_exception
from networksecurity.constants.training_pipeline import SAVE_MODEL_DIR, MODEL_FILE_NAME


class NetworkModel:
    def __init__(self, preprocessor, model):
        try:
            self.preprocessor = preprocessor
            self.model = model
        except Exception as e:
            raise custom_exception(e, sys)

    def predict(self, x):
        try:
            x_transform = self.preprocessor.transform(x)
            y_pred = self.model.predict(x_transform)
            return y_pred
        except Exception as e:
            raise custom_exception(e, sys)
        
    