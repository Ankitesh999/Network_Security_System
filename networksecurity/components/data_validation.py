import os
import sys
from scipy.stats import ks_2samp
import pandas as pd


from networksecurity.logging.logger import logger
from networksecurity.exception.exception import custom_exception

from networksecurity.entity.artifact_entity import DataIngestionArtifact, DataValidationArtifact
from networksecurity.entity.config_entity import DataValidationConfig
from networksecurity.constants.training_pipeline import SCHEMA_FILE_PATH
from networksecurity.utils.main_utils.utils import read_yaml_file, write_yaml_file

class DataValidation:
    def __init__(self, data_validation_config: DataValidationConfig, data_ingestion_artifact: DataIngestionArtifact):
        try:
            logger.info(f"{'>>'*20}Data Validation log started.{'<<'*20}")
            self.data_validation_config = data_validation_config
            self.data_ingestion_artifact = data_ingestion_artifact
            self.schema_config = read_yaml_file(SCHEMA_FILE_PATH)
        except Exception as e:
            raise custom_exception(e, sys) from e
        
    @staticmethod
    def read_data(file_path: str) -> pd.DataFrame:
        try:
            return pd.read_csv(file_path)
        except Exception as e:
            raise custom_exception(e, sys) from e
        
    def validate_number_of_columns(self, dataframe: pd.DataFrame) -> bool:
        try:
            expected_columns = self.schema_config['numerical_columns']
            actual_columns = list(dataframe.columns)
            return set(expected_columns) == set(actual_columns)
        except Exception as e:
            raise custom_exception(e, sys) from e
        
    def validate_numerical_columns_exist(self, dataframe: pd.DataFrame) -> bool:
        try:
            numerical_columns = self.schema_config['numerical_columns']
            for column in numerical_columns:
                if column not in dataframe.columns:
                    logger.error(f"Numerical column '{column}' is missing in the dataframe.")
                    return False
            return True
        except Exception as e:
            raise custom_exception(e, sys) from e
        
    def detect_data_drift(self, base_df: pd.DataFrame, current_df: pd.DataFrame, threshold: float = 0.05) -> bool:
        try:
            drift_detected = False
            report = {}
            for column in base_df.columns:
                base_data = base_df[column]
                current_data = current_df[column]
                ks_2result = ks_2samp(base_data, current_data)
                if ks_2result.pvalue < threshold:
                    is_drift = True
                    drift_detected = True
                    logger.info(f"Data drift detected for column: {column} (p-value: {ks_2result.pvalue})")
                else:
                    is_drift = False
                    logger.info(f"No data drift detected for column: {column} (p-value: {ks_2result.pvalue})")
                report.update({column: {"p_value": ks_2result.pvalue, "drift_status": is_drift}})

            drift_report_file_path = self.data_validation_config.drift_report_file_path
            dir_path = os.path.dirname(drift_report_file_path)
            os.makedirs(dir_path, exist_ok=True)

            write_yaml_file(file_path=drift_report_file_path, content=report)

            return drift_detected

        except Exception as e:
            raise custom_exception(e, sys) from e

    def initiate_data_validation(self) -> DataValidationArtifact:
        try:
            logger.info("Initiating data validation process.")
            train_file_path = self.data_ingestion_artifact.train_file_path
            test_file_path = self.data_ingestion_artifact.test_file_path

            logger.info("Reading training and testing data.")
            train_df = DataValidation.read_data(train_file_path)
            test_df = DataValidation.read_data(test_file_path)

            logger.info("Validating number of columns in training data.")
            if not self.validate_number_of_columns(train_df):
                raise ValueError("Training data does not have the expected number of columns.")
            
            logger.info("Validating number of columns in testing data.")
            if not self.validate_number_of_columns(test_df):
                raise ValueError("Testing data does not have the expected number of columns.")
            
            logger.info("Validating if numerical columns exists in training data.")
            if not self.validate_numerical_columns_exist(train_df):
                raise ValueError("Training data is missing some numerical columns.")
            
            logger.info("Validating if numerical columns exists in testing data.")
            if not self.validate_numerical_columns_exist(test_df):
                raise ValueError("Testing data is missing some numerical columns.")
            
            #if all checks pass, check data drift
            logger.info("Checking for data drift between training and testing data.")
            drift_detected = self.detect_data_drift(train_df, test_df)

            dir_path = os.path.dirname(self.data_validation_config.valid_train_file_path)
            os.makedirs(dir_path, exist_ok=True)

            dir_path = os.path.dirname(self.data_validation_config.valid_test_file_path)
            os.makedirs(dir_path, exist_ok=True)

            train_df.to_csv(self.data_validation_config.valid_train_file_path, index=False, header=True)
            test_df.to_csv(self.data_validation_config.valid_test_file_path, index=False, header=True)

            data_validation_artifact = DataValidationArtifact(
                validation_status=not drift_detected,  # True if no drift, False if drift detected
                valid_train_file_path=self.data_validation_config.valid_train_file_path,
                valid_test_file_path=self.data_validation_config.valid_test_file_path,
                invalid_train_file_path=self.data_validation_config.invalid_train_file_path,
                invalid_test_file_path=self.data_validation_config.invalid_test_file_path,
                drift_report_file_path=self.data_validation_config.drift_report_file_path
            )
            logger.info(f"Data validation artifact created: {data_validation_artifact}")
            return data_validation_artifact

        except Exception as e:
            logger.error(f"Error during data validation: {e}")
            raise custom_exception(e, sys) from e