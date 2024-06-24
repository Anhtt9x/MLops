import os
from src.logger.my_logging import logging
from src.exception.exception import customexception
import sys
import pandas as pd
from src.components.data_ingestion import DataIngestion
from src.components.data_transformation import DataTransformation
from src.components.model_trainer import ModelTrainer
from src.components.model_evaluation import ModelEvaluation

obj = DataIngestion()
train_path, test_path = obj.inititate_data_ingestion()

data_transformation = DataTransformation()
train_arr, test_arr = data_transformation.initialize_data_transformation(train_path=train_path,
                                                                         test_path=test_path)

model_trainer = ModelTrainer()
model_trainer.inititate_model_trainer(train_arr=train_arr,test_arr=test_arr)

model_evaluation = ModelEvaluation()
model_evaluation.initiate_model_eval(test_arr=test_arr)