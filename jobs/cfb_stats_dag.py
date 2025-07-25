"""
CFB Airflow DAG for Stats information
"""

from airflow.models.param import Param

from factories import DagFactory

BASE_URL = 'CFB_URL'
SECRET_VARIABLE = 'CFB_SECRET'
IDENTIFIER = 'cfb'
BUCKET_VARIABLE = 'CFB_BUCKET'

tags = ['stats']

PARAMETERS = {
    'schedule': Param(name='schedule', default='schedule/', type='string'),
    'temp': Param(name='temp', default='/airflow', type='string'),
}


dag = DagFactory.create_stats_dag(
    secret_name=SECRET_VARIABLE,
    identifier=IDENTIFIER,
    tags=tags,
    bucket=BUCKET_VARIABLE,
    url=BASE_URL,
    parameters=PARAMETERS

)
