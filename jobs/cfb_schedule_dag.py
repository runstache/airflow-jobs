"""
CFB Airflow DAG for Schedule information
"""

from datetime import datetime

from airflow.models.param import Param

from factories import DagFactory

BASE_URL = 'CFB_URL'
SECRET_VARIABLE = 'CFB_SECRET'
IDENTIFIER = 'cfb'
BUCKET_VARIABLE = 'CFB_BUCKET'

tags = ['schedule']

PARAMETERS = {
    'date': Param(name='date', default=datetime.now().strftime('%Y%m%d'), type='string'),
    'group': Param(name='group', default='80', type='string'),
    'week': Param(name='week', default='1', type='string'),
    'year': Param(name='year', default=datetime.now().strftime('%Y'), type='string'),
    'season': Param(name='season', default='2', type='string'),
    'temp': Param(name='temp', default='/airflow'),
}


dag = DagFactory.create_schedule_dag(
    secret_name=SECRET_VARIABLE,
    identifier=IDENTIFIER,
    tags=tags,
    bucket=BUCKET_VARIABLE,
    url=BASE_URL,
    parameters=PARAMETERS
)