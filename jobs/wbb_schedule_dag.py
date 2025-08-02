"""
WBB Airflow Stats Job DAG
"""

from datetime import datetime

from airflow.models.param import Param
from factories import DagFactory

BASE_URL = 'WBB_URL'
SECRET_VARIABLE_NAME = 'WBB_SECRET'
IDENTIFIER = 'wcbb'
BUCKET_VARIABLE = 'WBB_BUCKET'

tags = ['schedule']

PARAMETERS = {
    'date': Param(name='date', default=datetime.now().strftime('%Y%m%d'), type='string'),
    'group': Param(name='group', default='50', type='string'),
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
