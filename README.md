# Apache Airflow

This repository contains the configuration and jobs for my Airflow usage.

## Config

The configuration directory contains the install script and providers listing to install. This information is used for repeatable installation of the Airflow Application.

* install-script.sh:  Executes Installation through Pip using the constraints file and providers file
* providers.txt: Additional Providers to install.

## Jobs

This directory contains the airflow jobs being used.

### Helpers

The Helpers module is used for providing shared functions to be used by various DAG definitions.

### Factories

The Factories module contains a DagFactory that can be used to create common Stats and Schedule Jobs.

### Jobs

The following Jobs are available in the repository:

* WBB Schedule - Creates a Kubernetes Job to retrieve WCBB Schedule information and store in S3.
* WBB Stats - Creates Kubernetes Job to retrieve WCBB Stats information based on a Schedule file and stores it in S3.
* MLB Schedule - Creates a Kubernetes Job to retrieve the MLB Schedule information and store it in S3
* MLB Stats - Creates a Kubernetes Job to retrieve the MLB Stats for a given Schedule File and store them in S3.
* WNBA Schedule - Creates a Kubernetes Job to retrieve the WNBA Schedule information and store it in S3.
* WNBA Stats - Creates a Kubernetes Job to retrieve the WNBA Stats for a given Schedule file and store it in S3.
* CFB Schedule - Creates a Kubernetes Job to retrieve College Football Schedule information
* CFB Stats - Creates a Kubernetes job to retrieve College Football Stats Information

## Airflow Configuration

The current jobs leverage the following global variables:

* STAT_IMAGE: Docker Image name to use for the WBB Jobs
* WBB_SECRET: WBB Kubernetes Secret Name
* WBB_URL: Base Url to use for the WBB Stats retrieval
* WBB_BUCKET: S3 Bucket Name for the WBB Storage
* BASEBALL_SECRET: MLB Kubernetes Secret name
* BASEBALL_URL: Base Url for MLB Stats
* BASEBALL_BUCKET: Bucket name to store the MLB information
* WNBA_URL: Base url for retrieving WNBA information
* WNBA_SECRET: K8 Secret name for the WNBA workers
* WNBA_BUCKET: S3 bucket store the WNBA information
* CFB_URL: Base URL for CFB information
* CFB_BUCKET: S3 bucket name for CFB Stats
* CFB_SECRET: K8 Secret name for the CFB Workers
* NFL_URL: Base URL for NFL workers
* NFL_BUCKET: S3 Bucket name for the NFL Stats
* NFL_SECRET: K8 Secret name for the NFL Workers

Airflow also leverages a temp directory to write the Kubernetes Job definition to be used by the Kubernetes Job Operator. 
This path is provided at DAG Execution.

