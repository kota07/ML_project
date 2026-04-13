import os 
import sys

from src.exception import CustomException
from src.logger import logging
import pandas as pd
from sklearn.model_selection import train_test_split    
from dataclasses import dataclass


from src.compenents.data_transformation import DataTransformation
from src.compenents.data_transformation import DataTransformationConfig

@dataclass
class DataIngestionConfig:
    train_data_path: str = os.path.join("artifacts", "train.csv")
    test_data_path: str = os.path.join("artifacts", "test.csv")
    raw_data_path: str = os.path.join("artifacts", "data.csv")

class DataIngestion:
    def __init__(self):
        self.ingestion_config = DataIngestionConfig()

    def initiate_data_ingestion(self):
        logging.info("Entered the data ingestion method")
        try:
            df = pd.read_csv(os.path.join("notebook/data","stud.csv"))
            logging.info("Read the dataset as dataframe")

                        # Ensure all required directories exist
            for path in [
                self.ingestion_config.raw_data_path,
                self.ingestion_config.train_data_path,
                self.ingestion_config.test_data_path
            ]:
                os.makedirs(os.path.dirname(path), exist_ok=True)

            df.to_csv(self.ingestion_config.raw_data_path, index=False)
            logging.info("Saved the raw data to artifacts folder")  

            train_set, test_set = train_test_split(df, test_size=0.2, random_state=42)
            train_set.to_csv(self.ingestion_config.train_data_path, index=False, header=True)
            test_set.to_csv(self.ingestion_config.test_data_path, index=False, header=True) 
            logging.info("Saved the train and test data to artifacts folder")
            return (
                self.ingestion_config.train_data_path,
                self.ingestion_config.test_data_path
            )   
        
        except Exception as e:
            logging.info("Error occurred in data ingestion")
            raise CustomException(e, sys)   
        
if __name__ == "__main__":
    obj = DataIngestion()
    train_data,test_data=obj.initiate_data_ingestion()

    data_transformation_obj = DataTransformation()
    data_transformation_obj.initiate_data_transformation(train_data, test_data)






