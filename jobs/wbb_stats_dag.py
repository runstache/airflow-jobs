"""
WBB Airflow Stats Job
"""

from airflow.models.param import Param
from factories import DagFactory

BASE_URL = 'WBB_URL'
SECRET_VARIABLE_NAME = 'WBB_SECRET'
IDENTIFIER = 'wcbb'
BUCKET_VARIABLE = 'WBB_BUCKET'

tags = ['stats']

PARAMETERS = {
    'schedule': Param(name='schedule', default='schedule/', type='string'),
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
