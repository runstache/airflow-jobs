"""
WBB Airflow Stats Job
"""

import json
import os

from airflow import DAG
from airflow.models import Variable
from airflow.models.param import Param
from airflow.operators.python import PythonOperator
from airflow.providers.cncf.kubernetes.operators.job import KubernetesJobOperator
from uuid import uuid4

import helpers


def make_template(**context):
    """
    Generates the Template
    """
    print('Building Template')
    task_instance = context['ti']
    params = context['params']
    root = params['temp']
    job_spec = helpers.create_job_spec(Variable.get('WBB_SECRET'), 'wcbb-schedule-job',
                                       Variable.get('STAT_IMAGE'),
                                       ['python', 'stats_puller.py', '-b', params['bucket'],
                                        '-s', params['schedule']], Variable.get('WBB_URL'))

    output_path = os.path.join(root, 'templates')
    if not os.path.exists(output_path):
        os.makedirs(output_path)

    file_name = f"{str(uuid4())}-stats-job.json"
    with open(os.path.join(output_path, file_name), 'w') as f:
        json.dump(job_spec, f)

    task_instance.xcom_push(key='job-file',
                            value=os.path.join(output_path, file_name))


def clean_up_template(**context):
    """
    Cleans up the Template after Execution
    """

    task_instance = context['ti']
    path = task_instance.xcom_pull(task_ids='template-generator', key='job-file')
    if os.path.exists(path):
        os.remove(path)


with DAG(dag_id='wbb_stats_dag', schedule=None, catchup=False, tags=['stats'],
         params={
             'bucket': Param(name='bucket', default='wbb-stats-bucket', type='string'),
             'schedule': Param(name='schedule', default='schedule/', type='string'),
             'temp': Param(name='temp', default='/airflow', type='string')},
         default_args={'provider_context': True}):
    template = PythonOperator(task_id='template-generator',
                              python_callable=make_template)

    k8_job = KubernetesJobOperator(task_id='wbb-stat-job',
                                   job_template_file="{{ ti.xcom_pull(task_ids='template-generator', key='job-file') }}",
                                   backoff_limit=5,
                                   wait_until_job_complete=True, job_poll_interval=60,
                                   ttl_seconds_after_finished=300)

    clean_up = PythonOperator(task_id='clean-up-template',
                              python_callable=clean_up_template)

    template >> k8_job >> clean_up
