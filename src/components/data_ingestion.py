import os
import sys
from src.exception import CustomException
from src.logger import logging
import pandas as pd
from sklearn.model_selection import train_test_split
from dataclasses import dataclass
from src.components.data_transformation import DataTransformation
from src.components.data_transformation import DataTransformationConfig



@dataclass
# DataIngestionConfig - This is a configuration class that holds paths for train, test, and raw data.
# It uses the @dataclass decorator to automatically generate special methods like __init__().
class DataIngestionConfig:
    train_data_path : str = os.path.join('artifacts', 'train.csv')  #This joins folder name artifacts with file name train.csv
    test_data_path : str = os.path.join('artifacts', 'test.csv')  # Path to save the testing data.
    raw_data_path : str = os.path.join('artifacts', 'data.csv')


class DataIngestion:
    def __init__(self):
        self.ingestion_config = DataIngestionConfig()  # Initialize the configuration class.

    def initiate_data_ingestion(self):
        logging.info("Data Ingestion method starts")  # Log the start of the data ingestion process.
        try:
            df = pd.read_csv("notebook/stud.csv")
            logging.info("Read the dataset as dataframe")  # Log that the dataset has been read.
            os.makedirs(os.path.dirname(self.ingestion_config.train_data_path), exist_ok=True)  # Create directories if they do not exist.
            df.to_csv(self.ingestion_config.raw_data_path, index=False)  # Save the raw data to a CSV file.
            logging.info("Train test split initiated")  # Log that the train-test split is starting.
            train_set, test_set = train_test_split(df, test_size=0.2, random_state=42)  # Split the data into training and testing sets.
            train_set.to_csv(self.ingestion_config.train_data_path, index=False, header=True)  # Save the training set to a CSV file.
            test_set.to_csv(self.ingestion_config.test_data_path, index=False, header=True)  # Save the testing set to a CSV file.
            logging.info("Ingestion of data is completed")  # Log that the data ingestion process is complete.
            return (
                self.ingestion_config.train_data_path,
                self.ingestion_config.test_data_path,
                
            )
        except Exception as e:
            raise CustomException(e, sys)

if __name__ == "__main__":
    object = DataIngestion()  # Create an instance of the DataIngestion class.
    train_data, test_data = object.initiate_data_ingestion()  # Call the method to initiate data ingestion. 

    data_transformation = DataTransformation()
    data_transformation.initiate_data_transformation(train_data, test_data)            

# This code defines a DataIngestion class that handles the process of reading a dataset, splitting it into training and testing sets, and saving these sets to specified paths.
# It uses logging to track the progress and any issues that arise during the process. The configuration for file paths is managed using a dataclass.