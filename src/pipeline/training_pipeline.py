import os
from src.logger.my_logging import logging
from src.exception.exception import customexception
import sys
import pandas as pd
from src.components.data_ingestion import DataIngestion
from src.components.data_transformation import DataTransformation
from src.components.model_trainer import ModelTrainer
from src.components.model_evaluation import ModelEvaluation


class Training_And_Eval_PipeLine:
    def start_data_ingestion(self):
        try:
            obj = DataIngestion()
            train_path, test_path = obj.inititate_data_ingestion()
            return train_path, test_path
        except Exception as e:
            raise customexception(e,sys)
    
    def start_data_transform(self, train_path, test_path):
        try:
            data_transformation = DataTransformation()
            train_arr, test_arr = data_transformation.initialize_data_transformation(train_path=train_path,
                                                                                    test_path=test_path)
            return train_arr, test_arr
        except Exception as e:
            raise customexception(e,sys)
    
    def start_data_model_trainer(self,train_arr, test_arr):
        try:
            model_trainer = ModelTrainer()
            model_trainer.inititate_model_trainer(train_arr=train_arr,test_arr=test_arr)
        except Exception as e:
            raise customexception(e,sys)
    
    def start_data_model_eval(self, test_arr):
        try:
            model_evaluation = ModelEvaluation()
            model_evaluation.initiate_model_eval(test_arr=test_arr)
        except Exception as e:
            raise customexception(e,sys)
    
    def start_data_training_and_eval(self):
        try:
            train_path, test_path = self.start_data_ingestion()
            train_arr, test_arr = self.start_data_transform(train_path=train_path, test_path=test_path)
            self.start_data_model_trainer(train_arr=train_arr, test_arr=test_arr)
            self.start_data_model_eval(test_arr=test_arr)
        except Exception as e:
            raise customexception(e,sys)