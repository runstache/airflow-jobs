"""
Helper Functions for the application
"""


def create_job_spec(secret_name: str, job_name: str, image: str, commands: list[str], base_url:str) -> dict:
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
