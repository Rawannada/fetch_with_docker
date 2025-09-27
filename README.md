Amazon Books Data Pipeline with Airflow
This project implements an automated data pipeline that fetches book data from Amazon, processes it, stores it in MySQL, generates visualizations, and sends email reports using Apache Airflow in a Dockerized environment.

 Docker Setup
Project Structure with Docker:
```bash
fetch_with_docker/
├── dags/                    # Airflow DAG definitions
│   └── amazon_books_dag.py  # Main DAG file
├── docker-compose.yml       # Multi-container setup
├── Dockerfile              # Custom Airflow image
├── requirements.txt        # Python dependencies
└── README.md              # Documentation
```
Docker Services:
airflow-webserver: Airflow web interface (port 8080)

airflow-scheduler: Schedules and runs DAGs

postgres: Airflow metadata database

mysql: Book data storage database

redis: Message broker for Celery

 How to Run with Docker
1. Clone and Setup:
```bash
git clone <your-repository>
cd fetch_with_docker
```
2. Start Services:
```bash
docker-compose up --build
```
3. Access Airflow:
URL: http://localhost:8080

Credentials: airflow / airflow

4. Configure MySQL Connection in Airflow:
Go to Admin → Connections

Add new connection:

Conn Id: books_mysql_connection

Conn Type: MySQL

Host: mysql

Port: 3306

Database: booksdb 

Username: booksuser 

Password: bookspass 

5. Trigger DAG:
Navigate to DAGs page

Find fetch_and_store_amazon_books

Click "Trigger DAG"

 Pipeline Overview
The pipeline performs the following steps:

Fetch Data: Scrapes book data from Amazon search results

Clean & Transform: Processes and deduplicates book information

Database Operations: Creates MySQL table and inserts data

Visualization: Generates bar chart of top-rated books

Email Notification: Sends success/failure reports with visualization

 DAG Structure
Tasks:
create_table: Creates MySQL books table if not exists

fetch_book_data: Scrapes Amazon for data engineering books

clean_books: Cleans data and adds recommendation flags

insert_book_data: Stores processed data in MySQL

generate_visualization: Creates rating visualization chart

send_success_email: Sends success report with attachment

send_failure_email: Sends failure notification

Schedule:
Runs daily (schedule_interval=timedelta(days=1))

No catchup for missed runs

 Docker Commands
Useful Commands:
bash
# Check running containers
docker-compose ps

# View logs
docker-compose logs airflow-webserver
docker-compose logs airflow-scheduler

# Stop services
docker-compose down

# Stop and remove volumes
docker-compose down -v

# Restart specific service
docker-compose restart airflow-webserver
Database Persistence:
MySQL data persists in Docker volume

Airflow metadata in PostgreSQL volume

DAG files mounted from host to containers

 Data Model
MySQL Table Schema:
sql
CREATE TABLE books (
    id INT AUTO_INCREMENT PRIMARY KEY,
    title VARCHAR(255) NOT NULL,
    authors VARCHAR(255),
    rating FLOAT,
    recommended_flag VARCHAR(3)
);
Data Processing:
Deduplication: Removes duplicate books by title

Rating Conversion: Converts string ratings to numeric values

Recommendation Flag: Flags books with rating ≥ 4.0 as "Yes"

 Visualization Features
The pipeline generates a horizontal bar chart showing:

Top 10 books by rating

Cleaned and shortened book titles

Rating values displayed on bars

Professional styling with grid lines

High-quality PNG output (300 DPI)

 Email Notifications
Success Email:
Subject: "✅ Pipeline Succeeded"

Includes attached visualization PNG

Sent to: rwannada222@gmail.com

Failure Email:
Subject: "❌ Pipeline Failed"

Simple failure notification

Sent when any task fails

 Configuration
Docker Environment Variables:
AIRFLOW_UID: User ID for file permissions

_AIRFLOW_WWW_USER_USERNAME: Airflow username

_AIRFLOW_WWW_USER_PASSWORD: Airflow password

Required Connections:
books_mysql_connection: MySQL database connection

 Error Handling
Robust error handling for web scraping

Database insertion errors are logged but don't stop pipeline

Failure emails sent on any task failure

XCom data validation between tasks

 Troubleshooting
Common Issues:
Connection refused to MySQL:

Wait for MySQL container to fully start

Check MySQL logs: docker-compose logs mysql

DAG not appearing:

Check DAGs folder mount in docker-compose.yml

Restart airflow-webserver: docker-compose restart airflow-webserver

Import errors:

Ensure all packages in requirements.txt are installed

Rebuild images: docker-compose build --no-cache

 Notes
Uses BeautifulSoup for HTML parsing

Implements proper rate limiting (2-second delay)

Handles missing data gracefully

Includes comprehensive logging

Maintainer: Rawan Nada
Email: rwannada222@gmail.com

 Development Workflow
Edit DAG files in dags/ folder on host machine

Changes auto-sync to Airflow containers

Test DAGs in Airflow UI

Monitor logs using docker-compose commands

Deploy updates by pushing to repository

The Docker setup provides an isolated, reproducible environment for running your Airflow pipeline with all dependencies contained and managed automatically.