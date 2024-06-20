import numpy as np 
import pandas as pd 
import os
import sys
from pathlib import Path
from dataclasses import dataclass
from src.logger.my_logging import logging
from src.exception.exception import customexception
from src.utils.utils import save_object, evaluate_model
from sklearn.compose import ColumnTransformer
from sklearn.impute import SimpleImputer
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import OrdinalEncoder, StandardScaler


@dataclass
class DataTransformationConfig:
    preprocessing_obj_file_path = os.path.join("artifacts", "preprocess.pkl")

class DataTransformation:
    try:
        def __init__(self,):
            self.data_transformation = DataTransformationConfig()

        def get_data_transformation(self):
            try:
                logging.info("Data transformation initiate")

                num_colums = ['carat', 'depth', 'table', 'x', 'y', 'z']
                cat_colums = ['cut', 'color', 'clarity']

                cut_catagories = ["Fair", "Good", "Very Good", "Premium", "Ideal"]
                color_catagories = ["D", "E", "F", "G", "H", "I", "J"]
                clarity_catagories = ["I1", "SI2", "SI1", "VS2", "VS1", "VVS2", "VVS1", "IF"]

                logging.info("Pipeline initiate")

                numerical_pipeline = Pipeline([
                    ("impute",SimpleImputer(strategy="median")),
                    ("standard_scaler",StandardScaler())
                ])

                cat_pipeline = Pipeline([
                    ("impute",SimpleImputer(strategy="most_frequent")),
                    ("ordinal",OrdinalEncoder(categories=[cut_catagories,color_catagories,clarity_catagories]))
                ])

                preprocessor = ColumnTransformer([
                    ("num_pipeline",numerical_pipeline,num_colums),
                    ("cat_pipeline",cat_pipeline, cat_colums)
                ])

                return preprocessor

            except Exception as e:
                logging.info("Exception occured in the initiate_datatransformation")
                raise customexception(e,sys)

        def initialize_data_transformation(self,train_path, test_path):
            train_df = pd.read_csv(train_path)
            test_df = pd.read_csv(test_path)

            logging.info("read train and test data complete")
            logging.info(f"Train Datafram Head: \n{train_df.head().to_string()}")
            logging.info(f"Test Datafram Head: \n{test_df.head().to_string()}")

            preprocessing_obj = self.get_data_transformation()

            X_train = train_df.drop(["price", "id"], axis=1)
            y_train = train_df['price']

            X_test = test_df.drop(["price", "id"], axis=1)
            y_test = test_df['price']


            X_train_transform = preprocessing_obj.fit_transform(X_train)
            X_test_transform = preprocessing_obj.transform(X_test)

            logging.info("Applying preprocessing object on training and testing datasets.")

            train_arr = np.c_[X_train_transform,y_train]
            test_arr = np.c_[X_test_transform,y_test]

            save_object(file_path=self.data_transformation.preprocessing_obj_file_path,
                        obj=preprocessing_obj)

            logging.info("Preprocessing pickle saved file")

            return train_arr, test_arr
    
    except Exception as e:
        logging.info("Exception occured in the initiate_datatransformation")
        raise customexception(e,sys)
    

