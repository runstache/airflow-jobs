"""
Airflow Factories
"""

from airflow import DAG
from airflow.models import Variable
from airflow.operators.python import PythonOperator
from airflow.providers.cncf.kubernetes.operators.job import KubernetesJobOperator

import helpers


class DagFactory:
    """
    Factory to generate and provide Common DAG Instances
    """

    @staticmethod
    def create_schedule_dag(*, secret_name: str | None = None, identifier: str | None = None,
                            tags: list | None = None,
                            bucket: str | None = None,
                            url: str | None = None,
                            parameters:dict) -> DAG:
        """
        Creates a Schedule DAG
        :param secret_name: Name of Kubernetes Job Secret
        :param identifier: Dag identifier
        :param tags: Dag Tags
        :param bucket: Bucket Variable Name
        :param url: Base URL Variable Name
        :param parameters: Dag Parameters
        :return: DAG
        """
        if tags is None:
            tags = []


        with DAG(dag_id=f"{identifier}-schedule-dag", schedule=None, catchup=False, tags=tags,
                 params=parameters,
                 default_args={'provider_context': True}, max_active_runs=2) as schedule_dag:

            commands = [
                'python',
                'schedule_puller.py',
                '-b',
                Variable.get(bucket)]

            args = {
                'secret_name': secret_name,
                'job_name': f"{identifier}-schedule-job",
                'base_url': url,
                'commands': commands,
                'type': 'schedule'
            }

            template = PythonOperator(task_id='template-generator',
                                      python_callable=helpers.publish_template, op_kwargs=args)

            k8_job = KubernetesJobOperator(task_id=f"{identifier}-schedule-job",
                                           job_template_file="{{ ti.xcom_pull(task_ids='template-generator', key='job-file') }}",
                                           backoff_limit=5,
                                           wait_until_job_complete=True, job_poll_interval=60,
                                           ttl_seconds_after_finished=300)

            clean_up = PythonOperator(task_id='clean-up-template',
                                      python_callable=helpers.clean_up_templates)

            template >> k8_job >> clean_up

        return schedule_dag

    @staticmethod
    def create_stats_dag(*, secret_name: str | None = None,
                         identifier: str | None = None,
                         tags: list | None = None,
                         bucket:str | None = None,
                         url:str | None = None,
                         parameters: dict) -> DAG:
        """
        Creates a DAG for retrieving Statistics
        :param secret_name: Variable for the Secret Name
        :param identifier: Dag identifier
        :param tags: Tags
        :param bucket: Bucket Variable Name
        :param url: Base Url variable name
        :param parameters: DAG Parameters
        :return:
        """


        if not tags:
            tags = []


        with DAG(dag_id=f"{identifier}-stat-dag", schedule=None, catchup=False, tags=tags,
                 params=parameters,
                 default_args={'provider_context': True}, max_active_runs=1) as stat_dag:

            commands = ['python', 'stats_puller.py', '-b', Variable.get(bucket)]

            args = {
                'secret_name': secret_name,
                'job_name': f"{identifier}-stats-job",
                'base_url': url,
                'commands': commands,
                'type': 'stats'
            }

            template = PythonOperator(task_id='template-generator',
                                      python_callable=helpers.publish_template, op_kwargs=args)

            k8_job = KubernetesJobOperator(task_id=f"{identifier}-stats-job",
                                           job_template_file="{{ ti.xcom_pull(task_ids='template-generator', key='job-file') }}",
                                           backoff_limit=5,
                                           wait_until_job_complete=True, job_poll_interval=60,
                                           ttl_seconds_after_finished=300,
                                           log_events_on_failure=True, get_logs=True)

            clean_up = PythonOperator(task_id='clean-up-template',
                                      python_callable=helpers.clean_up_templates)

            template >> k8_job >> clean_up
        return stat_dag
