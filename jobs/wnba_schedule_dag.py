"""
Airflow DAG for pulling Schedule information for WNBA games
"""

from datetime import datetime

from airflow.models.param import Param

from factories import DagFactory

BASE_URL = 'WNBA_URL'
SECRET_VARIABLE = 'WNBA_SECRET'
IDENTIFIER = 'wnba'
BUCKET_VARIABLE = 'WNBA_BUCKET'

tags = ['schedule']

PARAMETERS = {
    'date': Param(name='date', default=datetime.now().strftime('%Y%m%d'), type='string'),
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
