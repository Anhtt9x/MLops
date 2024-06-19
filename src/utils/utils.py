import os 
import sys
import pickle
import numpy as np
import pandas as pd
from src.logger.my_logging import logging
from src.exception.exception import customexception
from sklearn.metrics import r2_score, mean_absolute_error ,mean_squared_error

def save_object(file_path, obj):
    try:
        dir_path = os.path.dirname(file_path)

        os.makedirs(dir_path,exist_ok=True)

        with open(dir_path,"wb") as f:
            pickle.dump(obj,f)

    except Exception as e:
        raise customexception(e,sys)
    
def load_object(file_path):
    try:
        with open(file_path, "rb") as f:
            pickle.load(f)

    except Exception as e:
        raise customexception(e,sys)
    
def evaluate_model(X_train,y_train,X_test,y_test,models):
    r2_list = {}
    try:
        for i in range(len(models)):
            model = list(models.values())[i]

            model.fit(X_train,y_train)

            y_pred = model.predict(X_test)

            test_score = r2_score(y_test,y_pred)

            r2_list[list(models.keys())[i]] = test_score

            return r2_list
        
    except Exception as e :
        logging.info('Exception occured during model training')
        raise customexception(e,sys)

    