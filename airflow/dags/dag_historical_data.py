from __future__ import annotations
from datetime import datetime, timedelta


import textwrap
import polars as pl
from src import HistoricalExtract
from airflow.models import Variable
from airflow.models.dag import DAG
from airflow.operators.python import PythonOperator


def get_data_callable():
    """
    Retrieves historical data and writes it to a parquet file.

    Returns:
        None
    """
    historical_extract = HistoricalExtract()
    data = historical_extract.get_data()
    data.write_parquet(
        r"/opt/airflow/temp/data/historical_data/historical_data.parquet"
    )


def persist_data_callable():
    """
    This function persists historical data to a PostgreSQL database.

    It reads the historical data from a Parquet file and calls the `persist_data` method
    of the `HistoricalExtract` class to store the data in the specified database.

    Parameters:
    - None

    Returns:
    - None
    """
    historical_data_polars = pl.read_parquet(
        r"/opt/airflow/temp/data/historical_data/historical_data.parquet"
    )
    historical_extract = HistoricalExtract()
    historical_extract.persist_data(
        dataframe=historical_data_polars,
        database="data_apps",
        db_user=Variable.get("POSTGRES_USER"),
        db_pass=Variable.get("POSTGRES_PASSWORD"),
        db_host="postgres_data_apps",
        db_port=5432,
    )


with DAG(
    "HistoricalData",
    default_args={
        "depends_on_past": False,
        "email": [""],
        "email_on_failure": False,
        "email_on_retry": False,
        "retries": 1,
        "retry_delay": timedelta(minutes=2),
        # 'queue': 'bash_queue',
        # 'pool': 'backfill',
        # 'priority_weight': 10,
        # 'end_date': datetime(2016, 1, 1),
        # 'wait_for_downstream': False,
        # 'sla': timedelta(hours=2),
        # 'execution_timeout': timedelta(seconds=300),
        # 'on_failure_callback': some_function, # or list of functions
        # 'on_success_callback': some_other_function, # or list of functions
        # 'on_retry_callback': another_function, # or list of functions
        # 'sla_miss_callback': yet_another_function, # or list of functions
        # 'trigger_rule': 'all_success'
    },
    description="Get Historical data from API",
    schedule=None,
    start_date=datetime(2024, 2, 4),
    catchup=False,
    tags=["Eventually"],
) as dag:
    get_historical_data = PythonOperator(
        python_callable=get_data_callable,
        task_id="historical_data",
        provide_context=True,
        dag=dag,
    )

    persist_historical_data = PythonOperator(
        python_callable=persist_data_callable,
        task_id="persist_historical_data",
        provide_context=True,
        dag=dag,
    )

    get_historical_data.doc_md = textwrap.dedent(
        """/
    #### Historical Data Documentation
    This task is responsible for extracting historical data from the API and persist to a database.
    """
    )

    dag.doc_md = __doc__
    dag.doc_md = """
    This is a documentation placed anywhere
    """
    persist_historical_data
