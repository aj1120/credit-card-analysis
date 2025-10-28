from datetime import timedelta
import uuid
from airflow.utils.dates import days_ago
from airflow import DAG
from airflow.providers.google.cloud.operators.dataproc import DataprocCreateBatchOperator
from airflow.providers.google.cloud.transfers.gcs_to_gcs import GCSToGCSOperator
from airflow.utils.trigger_rule import TriggerRule

# Default arguments

default_args = {
    "owner": "airflow",
    "depends_on_past": False,
    "start_date": days_ago(1),
    "retries": 1,
    "retry_delay": timedelta(minutes=5),
}


# DAG definition

with DAG(
    dag_id="credit_card_transactions_dataproc_dag",
    default_args=default_args,
    schedule_interval="0 5 * * *",   # Runs daily at 5 AM
    catchup=False,
    tags=["credit-card", "dataproc", "bq"],
) as dag:

   
    # GCS Configuration
  
    gcs_bucket = "avd-buck-credit-card-analysis"
    source_prefix = "transactions/"
    archive_prefix = "archive/"
    

    # Dataproc Configuration
  
    service_account = "dataproc-set@data-proc-468906.iam.gserviceaccount.com"
    project_id = "data-proc-468906"
    region = "us-central1"
    network_uri = f"projects/{project_id}/global/networks/default"
    subnetwork_uri = f"projects/{project_id}/regions/{region}/subnetworks/default"


    batch_id_users = f"load-users-batch-{uuid.uuid4().hex[:8]}"
    batch_id_txns = f"process-txns-batch-{uuid.uuid4().hex[:8]}"

    # 1️ Dataproc Job 1 — Load Users to BigQuery (Lightweight)
    load_users_task = DataprocCreateBatchOperator(
        task_id="load_users_to_bq",
        batch={
            "pyspark_batch": {
                "main_python_file_uri": f"gs://{gcs_bucket}/spark_job/load_users_to_bq.py"
            },
            "runtime_config": {
                "version": "2.2",
                "properties": {
                    # Use minimal resources
                    "spark.executor.instances": "1",
                    "spark.executor.cores": "1",
                    "spark.executor.memory": "1g",
                    "spark.driver.memory": "1g",
                },
            },
            "environment_config": {
                "execution_config": {
                    "service_account": service_account,
                    "network_uri": network_uri,
                    "subnetwork_uri": subnetwork_uri,
                }
            },
        },
        batch_id=batch_id_users,
        project_id=project_id,
        region=region,
        gcp_conn_id="google_cloud_default",
    )

    
    # 2️ Dataproc Job 2 — Process Credit Card Transactions

    process_txns_task = DataprocCreateBatchOperator(
        task_id="process_credit_card_txns",
        batch={
            "pyspark_batch": {
                "main_python_file_uri": f"gs://{gcs_bucket}/spark_job/spark_job.py"
            },
            "runtime_config": {
                "version": "2.2",
                "properties": {
                    # Slightly higher config for processing
                    "spark.executor.instances": "2",
                    "spark.executor.cores": "1",
                    "spark.executor.memory": "2g",
                    "spark.driver.memory": "2g",
                },
            },
            "environment_config": {
                "execution_config": {
                    "service_account": service_account,
                    "network_uri": network_uri,
                    "subnetwork_uri": subnetwork_uri,
                }
            },
        },
        batch_id=batch_id_txns,
        project_id=project_id,
        region=region,
        gcp_conn_id="google_cloud_default",
    )

    
    move_files_to_archive = GCSToGCSOperator(
        task_id="move_files_to_archive",
        source_bucket=gcs_bucket,
        source_object=source_prefix,
        destination_bucket=gcs_bucket,
        destination_object=archive_prefix,
        move_object=True,
        trigger_rule=TriggerRule.ALL_SUCCESS,
    )

   
    load_users_task >> process_txns_task >> move_files_to_archive
