AIRFLOW_VERSION=2.10.5
PYTHON_VERSION="$(python -c 'import sys; print(f"{sys.version_info.major}.{sys.version_info.minor}")')"
CONSTRAINT_URL="https://raw.githubusercontent.com/apache/airflow/constraints-${AIRFLOW_VERSION}/constraints-${PYTHON_VERSION}.txt"

echo "Installing Airflow"
pip3 install "apache-airflow==${AIRFLOW_VERSION}" --constraint $CONSTRAINT_URL

echo "Installing providers"
pip3 install -r providers.txt