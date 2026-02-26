import sys, os
import numpy as np
import pandas as pd
from sklearn.impute import KNNImputer
from sklearn.pipeline import Pipeline

from networksecurity.constants import training_pipeline
from networksecurity.entity.artifact_entity import DataTransformationArtifact, DataValidationArtifact
from networksecurity.entity.config_entity import DataTransformationConfig
from networksecurity.utils.main_utils.utils import save_numpy_array_data, save_object
from networksecurity.logging.logger import logger
from networksecurity.exception.exception import custom_exception


class DataTransformation:
    def __init__(self, data_transformation_config: DataTransformationConfig, data_validation_artifact: DataValidationArtifact):
        try:
            logger.info(f"{'>>'*20}Data Transformation log started.{'<<'*20} ")
            self.data_transformation_config = data_transformation_config
            self.data_validation_artifact = data_validation_artifact
        except Exception as e:
            raise custom_exception(e, sys)
        
    @staticmethod
    def read_data(file_path) -> pd.DataFrame:
        try:
            return pd.read_csv(file_path)
        except Exception as e:
            raise custom_exception(e, sys)

    def get_data_transformer_object(cls)->Pipeline:
        logger.info("Obtaining preprocessing object")
        try:
            imputer: KNNImputer = KNNImputer(**training_pipeline.DATA_TRANSFORMATION_IMPUTER_PARAMS)
            logger.info("Imputer object created")
            processor: Pipeline = Pipeline(steps=[('imputer', imputer)])
            return processor

        except Exception as e:
            raise custom_exception(e, sys)

    def initiate_data_transformation(self)->DataTransformationArtifact:
        logger.info("Initiating data transformation")
        try:
            train_file_path = self.data_validation_artifact.valid_train_file_path
            test_file_path = self.data_validation_artifact.valid_test_file_path

            train_df = DataTransformation.read_data(train_file_path)
            test_df = DataTransformation.read_data(test_file_path)

            input_feature_train_df = train_df.drop(columns=[training_pipeline.TARGET_COLUMN])
            target_feature_train_df = train_df[training_pipeline.TARGET_COLUMN]
            target_feature_train_df = target_feature_train_df.replace(-1, 0)

            input_feature_test_df = test_df.drop(columns=[training_pipeline.TARGET_COLUMN])
            target_feature_test_df = test_df[training_pipeline.TARGET_COLUMN]
            target_feature_test_df = target_feature_test_df.replace(-1, 0)

            preprocessor = self.get_data_transformer_object()
            preprocessor_object = preprocessor.fit(input_feature_train_df)
            transformed_input_train_features = preprocessor_object.transform(input_feature_train_df)
            transformed_input_test_features = preprocessor_object.transform(input_feature_test_df)

            train_arr = np.c_[transformed_input_train_features, np.array(target_feature_train_df)]
            test_arr = np.c_[transformed_input_test_features, np.array(target_feature_test_df)]

            save_numpy_array_data(file_path=self.data_transformation_config.transformed_train_file_path, array=train_arr)
            save_numpy_array_data(file_path=self.data_transformation_config.transformed_test_file_path, array=test_arr)
            save_object(file_path=self.data_transformation_config.transformed_object_file_path, obj=preprocessor_object)

            save_object("final_model/preprocessor.pkl", preprocessor_object)

            logger.info("Data transformation completed")

            data_transformation_artifact = DataTransformationArtifact(
            transformed_train_file_path=self.data_transformation_config.transformed_train_file_path,
            transformed_test_file_path=self.data_transformation_config.transformed_test_file_path,
            transformed_object_file_path=self.data_transformation_config.transformed_object_file_path)

            logger.info(f"Data transformation artifact: {data_transformation_artifact}")
            return data_transformation_artifact
        except Exception as e:
            logger.error(f"Error during data transformation: {e}")
            raise custom_exception(e, sys) from e


            



