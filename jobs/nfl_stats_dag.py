"""
Airflow DAG for NFL Stats
"""

from airflow.models.param import Param
from factories import DagFactory

BASE_URL = 'NFL_URL'
SECRET_VARIABLE_NAME = 'NFL_SECRET'
IDENTIFIER = 'nfl'
BUCKET_VARIABLE = 'NFL_BUCKET'

tags = ['stats']

PARAMETERS = {
    'schedule': Param(name='schedule', default='schedules/', type='string'),
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
