
from networksecurity.components.data_ingestion import DataIngestion
from networksecurity.components.data_validation import DataValidation
from networksecurity.components.data_transformation import DataTransformation
from networksecurity.exception.exception import custom_exception
from networksecurity.logging.logger import logger
from networksecurity.entity.config_entity import DataIngestionConfig, TrainingPipelineConfig, DataValidationConfig, DataTransformationConfig
import sys

if __name__ == "__main__":
    try:
        training_pipeline_config = TrainingPipelineConfig()
        data_ingestion_config = DataIngestionConfig(training_pipeline_config=training_pipeline_config)   
        data_validation_config = DataValidationConfig(training_pipeline_config=training_pipeline_config)
        data_transformation_config = DataTransformationConfig(training_pipeline_config=training_pipeline_config)

        data_ingestion = DataIngestion(data_ingestion_config=data_ingestion_config)
        data_ingestion_artifact = data_ingestion.initiate_data_ingestion()

        logger.info(f"Data Ingestion artifact: {data_ingestion_artifact}")

        data_validation = DataValidation(data_validation_config=data_validation_config, data_ingestion_artifact=data_ingestion_artifact)
        data_validation_artifact = data_validation.initiate_data_validation()
        
        logger.info(f"Data Validation artifact: {data_validation_artifact}")

        if not data_validation_artifact.validation_status:
            raise Exception("Data validation failed; aborting pipeline before transformation.")

        data_transformation = DataTransformation(data_transformation_config=data_transformation_config, data_validation_artifact=data_validation_artifact)
        data_transformation_artifact = data_transformation.initiate_data_transformation()
        logger.info(f"Data Transformation artifact: {data_transformation_artifact}")

    except Exception as e:
        raise custom_exception(e, sys) from e