import pandas as pd
import numpy as np
from src.logger.my_logging import logging
from src.exception.exception import customexception
import os
import sys
from dataclasses import dataclass
from pathlib import Path
from sklearn.compose import ColumnTransformer
from sklearn.impute import SimpleImputer
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import OrdinalEncoder, StandardScaler
from src.utils.utils import save_object
from sklearn.model_selection import train_test_split
@dataclass
class DataIngestionConfig:
    raw_path = os.path.join("artifacts/raw.csv")
    train_path = os.path.join("artifacts/train.csv")
    test_path = os.path.join("artifacts/test.csv")


class DataIngestion:
    def __init__(self,):
        self.ingestion_config = DataIngestionConfig()

    def inititate_data_ingestion(self):
        logging.info("data ingestion started")
        try:
            data = pd.read_csv("https://raw.githubusercontent.com/abhijitpaul0212/GemstonePricePrediction/master/notebooks/data/gemstone.csv")
            logging.info("reading data")

            os.makedirs(os.path.dirname(os.path.join(self.ingestion_config.raw_path)),exist_ok=True)
            data.to_csv(self.ingestion_config.raw_path, index=False)
            logging.info("i have saved the raw dataset in artifact folder")

            logging.info("here i have performed train test split")
            train_data, test_data = train_test_split(data, test_size=0.2)
            logging.info("train test split completed")

            os.makedirs(os.path.dirname(os.path.join(self.ingestion_config.train_path)),exist_ok=True)
            train_data.to_csv(self.ingestion_config.train_path,index=False)

            os.makedirs(os.path.dirname(os.path.join(self.ingestion_config.test_path)),exist_ok=True)
            test_data.to_csv(self.ingestion_config.test_path,index=False)
            logging.info("data ingestion part complete")

            return self.ingestion_config.train_path, self.ingestion_config.test_path

        except Exception as e:
            logging.info()
            raise customexception(e,sys)

    
if __name__ == "__main__":
    obj = DataIngestion()

    obj.inititate_data_ingestion()