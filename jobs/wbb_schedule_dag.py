"""
WBB Airflow Stats Job
"""

from datetime import datetime

from airflow import DAG
from airflow.models.param import Param
from airflow.providers.cncf.kubernetes.operators.job import KubernetesJobOperator
from kubernetes.client import models as k8s, V1PodTemplateSpec, V1PodSpec


def create_job_spec(secret_name: str, job_name: str, image: str, commands: list[str]) -> k8s.V1Job:
    """
    Job Template Spec Creation
    :param secret_name: Pod Sectet Name
    :param job_name: Job Name
    :param image: Docker Image
    :param commands: Commands
    :return: K8 Job
    """

    return k8s.V1Job(
        metadata=k8s.V1ObjectMeta(
            name=job_name
        ),
        spec=k8s.V1JobSpec(
            template=V1PodTemplateSpec(
                spec=V1PodSpec(
                    containers=[
                        k8s.V1Container(
                            name=job_name,
                            image=image,
                            command=commands,
                            env=[
                                k8s.V1EnvVar(
                                    name='AWS_ACCESS_KEY_ID',
                                    value_from=k8s.V1EnvVarSource(
                                        secret_key_ref=k8s.V1SecretKeySelector(
                                            name=secret_name,
                                            key='AWS_ACCESS_KEY_ID'
                                        )
                                    )
                                ),
                                k8s.V1EnvVar(
                                    name='AWS_SECRET_ACCESS_KEY',
                                    value_from=k8s.V1EnvVarSource(
                                        secret_key_ref=k8s.V1SecretKeySelector(
                                            name=secret_name,
                                            key='AWS_SECRET_ACCESS_KEY'
                                        )
                                    )
                                ),
                                k8s.V1EnvVar(
                                    name='S3_ENDPOINT',
                                    value_from=k8s.V1EnvVarSource(
                                        secret_key_ref=k8s.V1SecretKeySelector(
                                            name=secret_name,
                                            key='S3_ENDPOINT'
                                        )
                                    )
                                ),
                                k8s.V1EnvVar(
                                    name=secret_name,
                                    value_from=k8s.V1EnvVarSource(
                                        secret_key_ref=k8s.V1SecretKeySelector(
                                            name='wbb-worker-secrets',
                                            key='SELENIUM_DRIVER'
                                        )
                                    )
                                )
                            ]
                        )
                    ]
                )
            )
        )

    )


with DAG(
        dag_id='wcbb_schedule_download',
        description='Downloads',
        schedule_interval=None,
        params={
            'bucket': Param(name='bucket', default='wbb-stats-bucket', type='string'),
            'group': Param(name='group', default='50', type='string'),
            'date': Param(name='date', default=datetime.now().strftime('%Y%m%d'), type='string'),
            'image': Param(name='image', default='larrywshields/gen-stats-worker', type='string'),
            'secret': Param(name='secret', default='wbb-worker-secrets', type='string')
        }) as dag:
    job_template = create_job_spec(dag.params['secret'], dag.dag_id, dag.params['image'],
                                   ['python', 'schedule_puller.py', '-g',
                                    dag.params['group'], '-d', dag.params['date'], '-b',
                                    dag.params['bucket']])

    KubernetesJobOperator(full_job_spec=job_template, backoff_limit=5,
                          wait_until_job_complete=True, job_poll_interval=60,
                          config_file='/airflow/kubes/config', task_id='wcbb_schedule_puller')

if __name__ == '__main__':
    dag.test(group=50, date='20240101', image='larrywshields/gen-stats-worker',
             secret='wbb-worker-secrets')
