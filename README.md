# Apache Airflow

This repository contains the configuration and jobs for my Airflow usage.

## Config

The configuration directory contains the install script and providers listing to install. This information is used for repeatable installation of the Airflow Application.

* instal-script.sh:  Executes Installation through Pip using the constraints file and providers file
* providers.txt: Additional Providers to install.

## Jobs

This directory contains the airflow jobs being used.

### Helpers

The Helpers module is used for providing shared functions to be used by various DAG definitions.

### Jobs

The following Jobs are available in the repository:

* WBB Schedule - Creates a Kubernetes Job to retrieve WCBB Schedule information and store in S3.
* WBB Stats - Creates Kubernetes Job to retrieve WCBB Stats information based on a Schedule file and stores it in S3.

## Airflow Configuration

The current jobs leverage the following global variables:

* STAT_IMAGE: Docker Image name to use for the WBB Jobs
* WBB_SECRET: WBB Kubernetes Secret Name
* WBB_URL: Base Url to use for the WBB Stats retrieval

Airflow also leverages a temp directory to write the Kubenetes Job definition to be used by the Kubernetes Job Operator. 
This path is provided at DAG Execution.

