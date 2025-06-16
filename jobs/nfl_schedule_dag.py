"""
NFL Airflow DAG for schedule information
"""

from datetime import datetime

from airflow.models.param import Param

from factories import DagFactory

BASE_URL = 'NFL_URL'
SECRET_VARIABLE = 'NFL_SECRET'
IDENTIFIER = 'nfl'
BUCKET_VARIABLE = 'NFL_BUCKET'

tags = ['schedule']

PARAMETERS = {
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