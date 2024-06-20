import pandas as pd
import numpy as np
from src.logger.my_logging import logging
from src.exception.exception import customexception
import os
import sys
from dataclasses import dataclass
from pathlib import Path
from src.utils.utils import save_object ,evaluate_model
from sklearn.linear_model import LinearRegression, Ridge, Lasso, ElasticNet
@dataclass
class ModelTrainerConfig:
    trained_model_file_path = os.path.join("artifacts", "model.pkl")


class ModelTrainer:
    def __init__(self):
        self.model_trainer_config = ModelTrainerConfig()

    def inititate_model_trainer(self,train_arr, test_arr):
        try:
            logging.info("Split data")
            X_train = train_arr[:,:-1]
            y_train = train_arr[:,-1]
            X_test = test_arr[:,:-1]
            y_test = test_arr[:,-1]
            
            models = {
                "LinearRegression":LinearRegression(),
                "Ridge":Ridge(),
                "Lasso":Lasso(),
                "ElasticNet":ElasticNet()
            }

            trained_score:dict = evaluate_model(X_train=X_train,
                                                X_test=X_test,
                                                y_train=y_train,
                                                y_test= y_test,
                                                models=models)
            
            print(f"Trained_Score: {trained_score}")
            print("======================================")

            logging.info(f"Model trained score {trained_score}")
            
            best_trained_score = max(sorted(trained_score.values()))

            best_model_name = [k for k, v in trained_score.items() if v == best_trained_score]

            best_model_name = " ".join(best_model_name)

            best_model = models[best_model_name]
            

            print(f"Best model found: {best_model} and best score: {best_trained_score}")
            logging.info(f"Best model found: {best_model} and best score: {best_trained_score}")

            save_object(file_path=self.model_trainer_config.trained_model_file_path,
                        obj=best_model)
            
            

        except Exception as e:
            logging.info("Exception occured at Model training")
            raise customexception(e,sys)

    
