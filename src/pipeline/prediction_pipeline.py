import os
import sys
import pandas as pd
from src.exception.exception import customexception
from src.logger.my_logging import logging
from src.utils.utils import load_object
from dataclasses import dataclass


class PredictionPipeline:

    def __init__(self):
        print("init.. the object")
    
    def predict(self,feature):
        try:
            preprocessor_path = os.path.join("artifacts","preprocess.pkl")
            model_path = os.path.join("artifacts","model.pkl")

            preprocessor = load_object(preprocessor_path)
            model = load_object(model_path)

            scal_feature = preprocessor.transform(feature)
            pred=model.predict(scal_feature)

            return pred
        except Exception as e:
            raise customexception(e,sys)
    


class CustomData:
    def __init__(self,
                 carat:float,
                 depth:float,
                 table:float,
                 x:float,
                 y:float,
                 z:float,
                 cut:str,
                 color:str,
                 clarity:str):
        
        self.carat=carat
        self.depth=depth
        self.table=table
        self.x=x
        self.y=y
        self.z=z
        self.cut = cut
        self.color = color
        self.clarity = clarity


    def get_data_as_dataframe(self):
        try:
            custom_data_input_dict = {
                "cut":[self.cut],
                "carat":[self.carat],
                "color":[self.color],
                "clarity":[self.clarity],
                "table":[self.table],
                "x":[self.x],
                "y":[self.y],
                "z":[self.z],
                "depth":[self.depth]
            }

            df = pd.DataFrame(custom_data_input_dict)
            logging.info("DataFrame Gathered")
            return df
        
        except Exception as e:
            logging.info('Exception Occured in prediction pipeline')
            raise customexception(e,sys)