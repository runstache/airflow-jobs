"""
Hello World Dag
Verify Airflow is working
"""

from datetime import datetime

from airflow.sdk import DAG, task
from airflow.providers.standard.operators.empty import EmptyOperator
import logging

@task(task_id='h-task-1')
def log_it_out(**kwargs) -> str:
    """
    Logs the current time
    """

    logger = logging.getLogger(__name__)
    logger.info(datetime.now())
    return datetime.now().strftime('%Y-%m-%d %H:%M:%S')



with DAG(
    dag_id='hello_dag'
):

    ending = EmptyOperator(task_id='ending')
    ops = log_it_out()

    ops >> ending
