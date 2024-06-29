from __future__ import annotations
import json
from textwrap import dedent
import pendulum
from airflow import DAG
from airflow.operators.python import PythonOperator
from src.pipeline.training_pipeline import Training_And_Eval_PipeLine

train_and_eval = Training_And_Eval_PipeLine()

with DAG("gemstone_training_pipeline",
         default_args={"retries":2},
         description="it is my training pipeline",
         schedule="@weekly",
         start_date=pendulum.datetime(2024,1,17, tz="UTC"),
         catchup=False,
         tags=["machine_learning", "classification", "gemstone"]) as dag:
    
    dag.doc_md = __doc__

    def data_ingestion(**kwargs):
        ti = kwargs["ti"]
        train_data_path, test_data_path = train_and_eval.start_data_ingestion()
        ti.xcom_push("data_ingestion_artifact", {"train_data_path":train_data_path ,"test_data_path":test_data_path})

    def data_transformations(**kwargs):
        ti = kwargs["ti"]
        data_ingestion_artifact =ti.xcom_pull(task_ids="data_ingestion",key="data_ingestion_artifact")
        train_arr , test_arr = train_and_eval.start_data_transform(train_path=data_ingestion_artifact["train_data_path"], test_path= data_ingestion_artifact["test_data_path"])
        ti.xcom_push("data_transformations_artifacts", {"train_arr": train_arr, "test_arr":test_arr})

    def model_trainer(**kwargs):
        ti = kwargs["ti"]
        data_transformations_artifacts = ti.xcom_pull(task_ids="data_transformations", key="data_transformations_artifacts")
        train_arr=(data_transformations_artifacts["train_arr"])
        test_arr=(data_transformations_artifacts["test_arr"])
        train_and_eval.start_data_model_trainer(train_arr=train_arr, test_arr=test_arr)
        


    def push_data_to_s3(**kwargs):
        import os
        bucket_name = os.getenv("BUCKET_NAME")
        artifacts_folder = "app/artifacts"
        os.system(f"aws s3 sync {artifacts_folder} s3:/{bucket_name}/artifact")


    data_ingestion_task = PythonOperator(
        task_id="data_ingestion",
        python_callable=data_ingestion
    )
    data_ingestion_task.doc_md = dedent(
        """
    #### Ingestion task
    this task create a train and test file
        """
    )

    data_transformations_task = PythonOperator(
        task_id="data_transformations",
        python_callable=data_transformations
    )
    data_transformations_task.doc_md = dedent(
        """
    #### Transform task
    this task perform the transformation 
        """
    )

    model_trainer_task = PythonOperator(
        task_id = "model_trainer",
        python_callable=model_trainer
    )
    model_trainer_task.doc_md = dedent(
        """
    #### Trainer task
    this task train the model
        """
    )


    push_data_to_s3_task = PythonOperator(
        task_id="push_data_to_s3",
        python_callable=push_data_to_s3
    )
    push_data_to_s3_task.doc_md = dedent(
        """
    #### Pushdata task
    this task push data 
        """
    )

data_ingestion_task >> data_transformations_task >> model_trainer_task >> push_data_to_s3_task