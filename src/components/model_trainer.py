import pandas
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
from src.utils.utils import save_object ,evaluate_model
from sklearn.linear_model import LinearRegression, Ridge, Lasso, ElasticNet
@dataclass
class ModelTrainerConfig:
    pass

class ModelTrainer:
    def __init__(self,):
        pass

    def inititate_model_trainer(self):
        try:
            pass
        except Exception as e:
            logging.info()
            raise customexception(e,sys)

    
