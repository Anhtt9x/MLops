import os
import sys
from sklearn.metrics import mean_absolute_error, mean_squared_error
from urllib.parse import urlparse
import mlflow
import mlflow.sklearn
import numpy as np
import pickle
from src.utils.utils import load_object
from src.exception.exception import customexception
from dataclasses import dataclass
from src.logger.my_logging import logging
@dataclass
class ModelEvaluationConfig:
    pass

class ModelEvaluation:
    def __init__(self,):
        pass

    def inititate_model_evaluation(self):
        try:
            pass
        except Exception as e:
            logging.info()
            raise customexception(e,sys)

    
