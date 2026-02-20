import os
import sys
from scipy.stats import ks_2samp
import pandas as pd


from networksecurity.logging.logger import logger
from networksecurity.exception.exception import custom_exception

from networksecurity.entity.artifact_entity import DataIngestionArtifact, DataValidationArtifact
from networksecurity.entity.config_entity import DataValidationConfig
from networksecurity.constants.training_pipeline import SCHEMA_FILE_PATH
from networksecurity.utils.main_utils.utils import read_yaml_file

class DataValidation:
    def __init__(self, data_validation_config: DataValidationConfig, data_ingestion_artifact: DataIngestionArtifact):
        try:
            logger.info(f"{'>>'*20}Data Validation log started.{'<<'*20}")
            self.data_validation_config = data_validation_config
            self.data_ingestion_artifact = data_ingestion_artifact
            self.schema_config = read_yaml_file(SCHEMA_FILE_PATH)
            
        except Exception as e:
            raise custom_exception(e, sys) from e

