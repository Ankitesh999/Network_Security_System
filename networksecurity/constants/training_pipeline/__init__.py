#Common constants
import os


TARGET_COLUMN: str = "Result"
PIPELINE_NAME: str = "network_security_pipeline"
ARTIFACT_DIR: str = "artifacts"
FILE_NAME: str = "phishingDataset.csv"
SCHEMA_FILE_PATH: str = os.path.join("data_schema", "schema.yaml")

TRAIN_FILE_NAME: str = "train.csv"
TEST_FILE_NAME: str = "test.csv"

#Data Ingestion related constants
DATA_INGESTION_COLLECTION_NAME: str = "phishing_data"
DATA_INGESTION_DATABASE_NAME: str = "network_security_db"
DATA_INGESTION_DIR_NAME: str = "data_ingestion"
DATA_INGESTION_FEATURE_STORE_DIR: str = "feature_store"
DATA_INGESTION_INGESTED_DIR: str = "ingested"
DATA_INGESTION_TRAIN_TEST_SPLIT_RATIO: float = 0.2

#Data Validation related constants
DATA_VALIDATION_DIR_NAME: str = "data_validation"
DATA_VALIDATION_VALID_DIR: str = "valid"
DATA_VALIDATION_INVALID_DIR: str = "invalid"
DATA_VALIDATION_DRIFT_REPORT_DIR: str = "drift_report"
DRIFT_REPORT_FILE_NAME: str = "drift_report.yaml"