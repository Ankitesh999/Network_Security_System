from datetime import datetime
import os
from networksecurity.constants.training_pipeline import *

class TrainingPipelineConfig:
    def __init__(self, time_stamp: str = None):
        if time_stamp is None:
            time_stamp = datetime.now().strftime("%Y%m%d%H%M%S")

        self.pipeline_name = PIPELINE_NAME
        self.artifact_name = ARTIFACT_DIR
        self.artifact_dir = os.path.join(ARTIFACT_DIR, self.pipeline_name, time_stamp)
        self.time_stamp: str = time_stamp
        self.saved_model_dir = os.path.join(SAVE_MODEL_DIR)

class DataIngestionConfig:
    def __init__(self, training_pipeline_config: TrainingPipelineConfig):
        self.data_ingestion_dir = os.path.join(training_pipeline_config.artifact_dir, DATA_INGESTION_DIR_NAME)
        self.feature_store_file_path = os.path.join(self.data_ingestion_dir, DATA_INGESTION_FEATURE_STORE_DIR, FILE_NAME)       
        self.training_file_path = os.path.join(self.data_ingestion_dir, DATA_INGESTION_INGESTED_DIR, TRAIN_FILE_NAME)
        self.testing_file_path = os.path.join(self.data_ingestion_dir, DATA_INGESTION_INGESTED_DIR, TEST_FILE_NAME)
        self.train_test_split_ratio: float = DATA_INGESTION_TRAIN_TEST_SPLIT_RATIO
        self.collection_name: str = DATA_INGESTION_COLLECTION_NAME
        self.database_name: str = DATA_INGESTION_DATABASE_NAME

class DataValidationConfig:
    def __init__(self, training_pipeline_config: TrainingPipelineConfig):
        self.data_validation_dir = os.path.join(training_pipeline_config.artifact_dir, DATA_VALIDATION_DIR_NAME)
        self.valid_data_dir = os.path.join(self.data_validation_dir, DATA_VALIDATION_VALID_DIR)
        self.invalid_data_dir = os.path.join(self.data_validation_dir, DATA_VALIDATION_INVALID_DIR)
        self.valid_train_file_path = os.path.join(self.valid_data_dir, TRAIN_FILE_NAME)
        self.valid_test_file_path = os.path.join(self.valid_data_dir, TEST_FILE_NAME)
        self.invalid_train_file_path = os.path.join(self.invalid_data_dir, TRAIN_FILE_NAME)
        self.invalid_test_file_path = os.path.join(self.invalid_data_dir, TEST_FILE_NAME)
        self.drift_report_file_path = os.path.join(self.data_validation_dir, DATA_VALIDATION_DRIFT_REPORT_DIR, DRIFT_REPORT_FILE_NAME)

class DataTransformationConfig:
    def __init__(self, training_pipeline_config: TrainingPipelineConfig ):
        self.data_transformation_dir = os.path.join(training_pipeline_config.artifact_dir, DATA_TRANSFORMATION_DIR_NAME, )
        self.transformed_train_file_path = os.path.join(self.data_transformation_dir, DATA_TRANSFORMATION_TRANSFORMED_DIR, TRAIN_FILE_NAME.replace("csv", "npy"))
        self.transformed_test_file_path = os.path.join(self.data_transformation_dir, DATA_TRANSFORMATION_TRANSFORMED_DIR, TEST_FILE_NAME.replace("csv", "npy"))    
        self.transformed_object_file_path = os.path.join(self.data_transformation_dir, DATA_TRANSFORMATION_TRANSFORMED_OBJECT_DIR, PREPROCESSING_OBJECT_FILE_NAME)

class ModelTrainerConfig:
    def __init__(self, training_pipeline_config: TrainingPipelineConfig):
        self.model_trainer_dir = os.path.join(training_pipeline_config.artifact_dir, MODEL_TRAINER_DIR_NAME)
        self.trained_model_file_path = os.path.join(self.model_trainer_dir, MODEL_TRAINER_TRAINED_MODEL_DIR, MODEL_FILE_NAME)
        self.expected_accuracy = MODEL_TRAINER_EXPECTED_ACCURACY
        self.overfitting_underfitting_threshold = MODEL_TRAINER_OVERFITTING_UNDERFITTING_THRESHOLD
    


