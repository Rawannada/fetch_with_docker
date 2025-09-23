Fetch Data with Airflow & Docker
This project demonstrates how to automate data fetching, processing, and storage workflows using Apache Airflow within a containerized environment powered by Docker Compose. This setup integrates PostgreSQL, MySQL, and Redis services with Airflow to create a robust data pipeline.

Features
Airflow DAGs: Automated workflows for fetching and processing data.

PostgreSQL: Serves as the metadata database for Airflow, managing all workflow states.

MySQL: A dedicated database for storing project-specific data, such as a books database.

Redis: Used for caching, message brokering, or as a key-value store to support specific tasks.

Containerized Environment: Simplifies setup and deployment across different systems using Docker Compose.

Scalable Architecture: Designed to be easily extended with new DAGs, operators, or plugins.

Project Structure
```bash
fetch_with_docker/
├── dags/                # Airflow DAG definitions
├── data/                # Raw data (ignored in Git)
├── processed_data/      # Cleaned/processed data
├── plugins/             # Custom Airflow plugins
├── logs/                # Airflow logs (ignored in Git)
├── Dockerfile           # Custom Docker image definition
├── docker-compose.yml   # Docker services configuration
├── requirements.txt     # Python dependencies
├── .gitignore           # Specifies files and folders to ignore
└── README.md            # Project documentation
```
Requirements
Docker: The core platform for containerization.

Docker Compose: To orchestrate and run the multi-container application.

Python 3.9+: For developing and writing Airflow DAGs.

Setup & Run
Follow these simple steps to get the project up and running on your machine:

Clone the repository:

```Bash

git clone https://github.com/Rawannada/fetch_data_airflow.git
cd fetch_data_airflow
```
Build and start all services:
This command will build the Docker images and start all the services defined in docker-compose.yml.

```Bash

docker-compose up --build
```
Access the Airflow UI:
Open your web browser and navigate to the following URL:

URL: http://localhost:8080

Default Credentials: airflow / airflow

Trigger the DAG:

Go to the Airflow UI.

Navigate to the DAGs page.

Find the fetch_dag_docker and click the "Trigger DAG" button.

Services Overview
Service	Description
postgres	The PostgreSQL database for Airflow's metadata.
mysql	The MySQL database for storing project data.
redis	The Redis cache/message broker service.
airflow-webserver	The Airflow web interface for managing DAGs.
airflow-scheduler	The service that schedules and triggers DAGs.
Note: All database and Airflow data are persisted using Docker volumes, ensuring that your data remains intact even if containers are stopped or restarted.

Notes
Sensitive files and data, such as .env files, raw data, logs, and database files, are excluded from Git via the .gitignore file.

To add new workflows, simply create a new Python file under the dags/ directory.

For custom logic or operators, add your code to the plugins/ folder.

Author
Rawan Nada

Email: Rwannada22@gmail.com

LinkedIn: Rawan Nada