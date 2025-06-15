"""
Helper Functions for the application
"""
import json
import logging
import os
import uuid

from airflow.models import Variable


def create_job_spec(secret_name: str, job_name: str, image: str, commands: list[str],
                    base_url: str) -> dict:
    """
    Job Template Spec Creation
    :param secret_name: Pod Secret Name
    :param job_name: Job Name
    :param image: Docker Image
    :param commands: Commands
    :param base_url: Base Url
    :return: K8 Job
    """
    return {
        "apiVersion": "batch/v1",
        "kind": "Job",
        "metadata": {
            "name": job_name
        },
        "spec": {
            "template": {
                "spec": {
                    "containers": [
                        {
                            "name": job_name,
                            "image": image,
                            "command": commands,
                            "env": [
                                {
                                    "name": "AWS_ACCESS_KEY_ID",
                                    "valueFrom": {
                                        "secretKeyRef": {
                                            "name": secret_name,
                                            "key": "AWS_ACCESS_KEY_ID"

                                        }
                                    }
                                },
                                {
                                    "name": "AWS_SECRET_ACCESS_KEY",
                                    "valueFrom": {
                                        "secretKeyRef": {
                                            "name": secret_name,
                                            "key": "AWS_SECRET_ACCESS_KEY"

                                        }
                                    }
                                },
                                {
                                    "name": "S3_ENDPOINT",
                                    "valueFrom": {
                                        "secretKeyRef": {
                                            "name": secret_name,
                                            "key": "S3_ENDPOINT"

                                        }
                                    }
                                },
                                {
                                    "name": "SELENIUM_DRIVER",
                                    "valueFrom": {
                                        "secretKeyRef": {
                                            "name": secret_name,
                                            "key": "SELENIUM_DRIVER"

                                        }
                                    }
                                },
                                {
                                    "name": "BASE_URL",
                                    "value": base_url
                                }
                            ]
                        }
                    ],
                    "restartPolicy": "Never"
                },
                "backoffPolicy": 4,
                "ttlSecondsAfterFinished": 300
            }
        }

    }


def publish_template(**kwargs):
    """
    Publishes the Job Template to the Temp Directory
    """

    logger = logging.getLogger(__name__)
    logger.info('Building Template')

    task_instance = kwargs['ti']
    params = kwargs['params']
    root = params['temp']

    commands:list = kwargs['commands']

    if 'date' in params:
        commands.append('-d')
        commands.append(params['date'])

    if 'group' in params:
        commands.append('-g')
        commands.append(params['group'])

    if 'schedule' in params:
        commands.append('-s')
        commands.append(params['schedule'])

    if 'week' in params:
        commands.append('-w')
        commands.append(params['week'])

    if 'year' in params:
        commands.append('-y')
        commands.append(params['year'])

    if 'season' in params:
        commands.append('-s')
        commands.append(params['season'])

    job_spec = create_job_spec(Variable.get(kwargs['secret_name']), kwargs['job_name'],
                               Variable.get('STAT_IMAGE'),
                               commands,
                               Variable.get(kwargs['base_url']))

    output_path = os.path.join(root, 'templates')

    if not os.path.exists(output_path):
        os.makedirs(output_path)

    file_name = f"{uuid.uuid4()}-{kwargs['job_name']}-{kwargs['type']}-job.json"
    with open(os.path.join(output_path, file_name), 'w') as f:
        json.dump(job_spec, f)

    task_instance.xcom_push(key='job-file',
                            value=os.path.join(output_path, file_name))


def clean_up_templates(**kwargs):
    """
    Cleans up the Temp Directory
    """

    task_instance = kwargs['ti']
    path = task_instance.xcom_pull(task_ids='template-generator', key='job-file')
    if os.path.exists(path):
        os.remove(path)
