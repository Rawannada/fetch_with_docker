Fetch & Process Amazon Books with Airflow & Docker

This project demonstrates how to automate the fetching, cleaning, transformation, and storage of book data from Amazon using Apache Airflow within a Docker Compose environment. The pipeline integrates MySQL, PostgreSQL, and Redis to create a robust, scalable workflow.

Features

Automated Workflows (DAGs): Fetch, clean, and insert book data automatically.

Data Cleaning & Transformation:

Removes duplicate books.

Converts ratings to float.

Adds recommended_flag column (Yes if rating ≥ 4.0, No otherwise).

MySQL Storage: Stores structured book data with title, author, rating, and recommended_flag.

Email Notifications: Sends success or failure emails after pipeline completion.

Containerized Environment: Docker Compose integrates Airflow, MySQL, PostgreSQL, and Redis.

Scalable Architecture: Easily add new DAGs, operators, or plugins.
```bash
Project Structure
fetch_with_docker/
├── dags/                # Airflow DAG definitions
├── data/                # Raw data (ignored in Git)
├── processed_data/      # Cleaned/processed data
├── plugins/             # Custom Airflow plugins
├── logs/                # Airflow logs (ignored in Git)
├── Dockerfile           # Custom Docker image definition
├── docker-compose.yml   # Docker services configuration
├── requirements.txt     # Python dependencies
├── .gitignore           # Specifies files/folders to ignore
└── README.md            # Project documentation
```
Requirements

Docker: Core platform for containerization.

Docker Compose: Orchestrates multi-container setup.

Python 3.9+: Develop and run Airflow DAGs.

Setup & Run

Clone the repository:
```bash
git clone https://github.com/Rawannada/fetch_data_airflow.git
cd fetch_data_airflow
```

Build and start services:
```bash

docker-compose up --build
```

Access the Airflow UI:

URL: http://localhost:8080

Default Credentials: airflow / airflow

Trigger the DAG:

Navigate to the DAGs page in the Airflow UI.

Find fetch_and_store_amazon_books and click Trigger DAG.

Services Overview
Service	Description
postgres	Metadata database for Airflow
mysql	Stores project-specific book data
redis	Caching and message brokering
airflow-webserver	Airflow UI
airflow-scheduler	Schedules and triggers DAGs

All database and Airflow data are persisted using Docker volumes.

Notes

Sensitive files (.env, logs, raw data, database files) are excluded via .gitignore.

To add new workflows, create a new Python file in dags/.

For custom logic/operators, use the plugins/ folder.

Author

Rawan Nada

Email: Rwannada22@gmail.com

LinkedIn: https://www.linkedin.com/in/rawan-nada-a63994281