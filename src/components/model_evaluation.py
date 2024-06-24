import os
import sys
from sklearn.metrics import mean_absolute_error, mean_squared_error, r2_score
from urllib.parse import urlparse
import mlflow
import mlflow.sklearn
from mlflow.models import infer_signature
import numpy as np
import pickle
from src.utils.utils import load_object
from src.exception.exception import customexception
from src.logger.my_logging import logging
import dagshub


class ModelEvaluation:
    def __init__(self,):
        logging.info("Evaluation Started")

    def eval_metrics(self, y_true, y_pred):
        rmse = np.sqrt(mean_squared_error(y_true=y_true, y_pred=y_pred))
        mae = mean_absolute_error(y_true=y_true, y_pred=y_pred)
        r2 = r2_score(y_true=y_true, y_pred=y_pred)
        logging.info("Evaluation metrics")

        return rmse, mae, r2

    
    def initiate_model_eval(self, test_arr):
        try:
            X_test, y_test = test_arr[:,:-1], test_arr[:,-1]
            model_path = os.path.join("artifacts", "model.pkl")

            model=load_object(model_path)

            dagshub.init(repo_owner='Anhtt9x', repo_name='MLops', mlflow=True)


            tracking_url_type_store=urlparse(mlflow.get_tracking_uri()).scheme
            print(tracking_url_type_store)

            with mlflow.start_run():
                pred=model.predict(X_test)
                rmse, mae, r2=self.eval_metrics(y_true=y_test, y_pred=pred)
                signature = infer_signature(X_test, pred)

                mlflow.log_metric("rmse",rmse)
                mlflow.log_metric("mae",mae)
                mlflow.log_metric("r2_score",r2)

                if tracking_url_type_store != "file":
                    mlflow.sklearn.log_model(model, "model", registered_model_name="mlmodel", signature=signature)
                else:
                    mlflow.sklearn.log_model(model, "model", signature=signature)
        except Exception as e:
            logging.info("")
            raise customexception(e,sys)