import os
import sys
import numpy as np
import pandas as pd

from networksecurity.logging.logger import logger
from networksecurity.exception.exception import custom_exception
from networksecurity.entity.config_entity import DataIngestionConfig
from networksecurity.entity.artifact_entity import DataIngestionArtifact

import pymongo
from typing import List
from sklearn.model_selection import train_test_split
from dotenv import load_dotenv
load_dotenv()

MONGO_DB_URL_KEY = os.getenv("MONGO_DB_URI")

class DataIngestion:
    def __init__(self, data_ingestion_config: DataIngestionConfig):

        try:
            logger.info(f"{'>>'*20}Data Ingestion log started.{'<<'*20} ")
            self.data_ingestion_config = data_ingestion_config

        except Exception as e:
            raise custom_exception(str(e), sys)
            
    def export_collection_as_dataframe(self):
        #read data from mongoDB and store it in a pandas dataframe
        try:
            logger.info(f"Exporting collection data as pandas dataframe")

            database_name = self.data_ingestion_config.database_name
            collection_name = self.data_ingestion_config.collection_name

            self.mongo_client = pymongo.MongoClient(MONGO_DB_URL_KEY)

            db = self.mongo_client[database_name]
            collection = db[collection_name]
            
            df = pd.DataFrame(list(collection.find()))
            if "_id" in df.columns.to_list():
                df = df.drop("_id", axis=1)
            df.replace({"na": np.nan}, inplace=True)    

            self.mongo_client.close()

            return df
        
        except Exception as e:
            raise custom_exception(str(e), sys) from e
    
    def export_data_into_feature_store(self, df: pd.DataFrame):
        try:
            logger.info(f"Exporting data into feature store")

            feature_store_file_path = os.path.dirname(self.data_ingestion_config.feature_store_file_path)

            dir_path = os.path.dirname(feature_store_file_path)

            os.makedirs(dir_path, exist_ok=True)

            df.to_csv(feature_store_file_path, index=False, header=True)
            return df

        except Exception as e:
            raise custom_exception(str(e), sys) from e
        
    def split_data_as_train_test(self, df: pd.DataFrame):
        try:
            logger.info(f"Splitting data into train and test set")

            train_set, test_set = train_test_split(df, test_size=self.data_ingestion_config.train_test_split_ratio, random_state=42)

            train_file_path = self.data_ingestion_config.training_file_path
            test_file_path = self.data_ingestion_config.testing_file_path

            dir_path = os.path.dirname(train_file_path)
            os.makedirs(dir_path, exist_ok=True)

            dir_path = os.path.dirname(test_file_path)
            os.makedirs(dir_path, exist_ok=True)

            train_set.to_csv(train_file_path, index=False, header=True)
            test_set.to_csv(test_file_path, index=False, header=True)

            logger.info(f"Data split into train and test set successfully")
        except Exception as e:
            raise custom_exception(str(e), sys) from e

    def initiate_data_ingestion(self):
        try:
            df = self.export_collection_as_dataframe()
            df = self.export_data_into_feature_store(df)
            self.split_data_as_train_test(df)
            data_ingestion_artifact = DataIngestionArtifact(train_file_path=self.data_ingestion_config.training_file_path, test_file_path=self.data_ingestion_config.testing_file_path)

            return data_ingestion_artifact

        except Exception as e:
            raise custom_exception(str(e), sys) from e


