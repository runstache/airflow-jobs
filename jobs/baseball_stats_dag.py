"""
MLB Airflow Stats DAG
"""

from airflow.models.param import Param
from factories import DagFactory

BASE_URL = 'BASEBALL_URL'
SECRET_VARIABLE_NAME = 'BASEBALL_SECRET'
IDENTIFIER = 'mlb'
BUCKET_VARIABLE = 'BASEBALL_BUCKET'

tags = ['stats']

PARAMETERS = {
    'schedule': Param(name='date', default='schedule/', type='string'),
    'temp': Param(name='temp', default='/airflow', type='string'),
}


dag = DagFactory.create_stats_dag(
    secret_name=SECRET_VARIABLE_NAME,
    identifier=IDENTIFIER,
    tags=tags,
    bucket=BUCKET_VARIABLE,
    url=BASE_URL,
    parameters=PARAMETERS,
)
