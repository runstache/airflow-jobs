"""
MLB Schedule Job DAG
"""

from datetime import datetime

from airflow.models.param import Param
from factories import DagFactory

BASE_URL = 'BASEBALL_URL'
SECRET_VARIABLE_NAME = 'BASEBALL_SECRET'
IDENTIFIER = 'mlb'
BUCKET_VARIABLE = 'BASEBALL_BUCKET'

tags = ['schedule']

PARAMETERS = {
    'date': Param(name='date', default=datetime.now().strftime('%Y%m%d'), type='string'),
    'temp': Param(name='temp', default='/airflow'),
}


dag = DagFactory.create_schedule_dag(
    secret_name=SECRET_VARIABLE_NAME,
    identifier=IDENTIFIER,
    tags=tags,
    bucket=BUCKET_VARIABLE,
    url=BASE_URL,
    parameters=PARAMETERS,
)
