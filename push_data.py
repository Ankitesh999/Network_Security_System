
import os
import sys
import json

from networksecurity.logging.logger import logger
from networksecurity.exception import exception

import pandas as pd
import numpy as np
import pymongo

from dotenv import load_dotenv
load_dotenv()

MONGO_DB_URI = os.getenv("MONGO_DB_URI")
if not MONGO_DB_URI:
    raise RuntimeError("MONGO_DB_URI environment variable is not set. Please set it in your environment or .env file.")

import certifi
ca = certifi.where()

class DataExtractor:


    def __init__(self, mongo_uri: str = MONGO_DB_URI):
        try:
            self.client = pymongo.MongoClient(mongo_uri, tlsCAFile=ca)
        except Exception as e:
            logger.error(f"Failed to connect to MongoDB: {e}")
            raise exception.custom_exception("MongoDB connection error", sys) from e

        # Validate connection separately
        try:
            self.client.admin.command("ping")
            logger.info("Successfully connected to MongoDB.")
        except Exception as ping_err:
            logger.error(f"Failed to ping MongoDB: {ping_err}")
            raise exception.custom_exception("MongoDB ping error", sys) from ping_err
        

    def csv_to_json(self, csv_file_path: str, json_file_path: str):
        try:
            df = pd.read_csv(csv_file_path)
            df.reset_index(drop=True, inplace=True)
            data = list(json.loads(df.T.to_json()).values())
            # Write JSON output to file
            with open(json_file_path, 'w', encoding='utf-8') as jf:
                json.dump(data, jf, ensure_ascii=False, indent=4)
            logger.info(f"Successfully converted {csv_file_path} to {json_file_path}")
            return data
        except Exception as e:
            logger.error(f"Error converting CSV to JSON: {e}")
            raise exception.custom_exception("CSV to JSON conversion error", sys) from e
        

    def insert_data_to_mongodb(self, data: list, db_name: str, collection_name: str):
        try:
            # Input validation
            if not isinstance(data, list):
                logger.error("Data must be a list of dictionaries.")
                raise exception.custom_exception("Data format error: not a list", sys)
            if not data:
                logger.error("No data to insert into MongoDB.")
                raise exception.custom_exception("No data to insert into MongoDB", sys)

            self.database = db_name
            self.collection_name = collection_name
            self.data = data

            # Use existing client
            self.db = self.client[db_name]
            self.collection = self.db[collection_name]

            self.collection.insert_many(data)
            logger.info(f"Successfully inserted data into {db_name}.{collection_name}")
            return (len(data), f"Data inserted into {db_name}.{collection_name} successfully.")
        except Exception as e:
            logger.error(f"Error inserting data into MongoDB: {e}")
            raise exception.custom_exception("MongoDB insertion error", sys) from e
        
    
        
if __name__ == "__main__":
    FILE_PATH = "data/phishingDataset.csv"
    DATABASE_NAME = "network_security_db"
    COLLECTION_NAME = "phishing_data"
    try:
        if not os.path.exists(FILE_PATH):
            logger.error(f"CSV file not found: {FILE_PATH}")
            raise exception.custom_exception(f"CSV file not found: {FILE_PATH}", sys)
        extractor = DataExtractor()
        data = extractor.csv_to_json(FILE_PATH, f"data/{COLLECTION_NAME}.json")
        extractor.insert_data_to_mongodb(data, DATABASE_NAME, COLLECTION_NAME)
        logger.info("Data extraction and insertion completed successfully.")
    except exception.custom_exception as e:
        logger.error(f"Error during data extraction and insertion: {e}")
        print(e)

