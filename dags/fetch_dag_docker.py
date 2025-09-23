from datetime import datetime, timedelta
from airflow import DAG
from airflow.operators.python import PythonOperator
from airflow.providers.mysql.hooks.mysql import MySqlHook
from airflow.operators.email import EmailOperator  # استيراد الـ EmailOperator
import requests
import time
from bs4 import BeautifulSoup

# ======= Updated headers + cookies =======
headers = {
    "authority": "www.amazon.com",
    "accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8",
    "accept-language": "en-US,en;q=0.9",
    "cache-control": "no-cache",
    "pragma": "no-cache",
    "referer": "https://www.amazon.com/",
    "sec-ch-ua": '"Chromium";v="124", "Google Chrome";v="124", "Not=A?Brand";v="24"',
    "sec-ch-ua-mobile": "?0",
    "sec-ch-ua-platform": '"Windows"',
    "upgrade-insecure-requests": "1",
    "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
                  "AppleWebKit/537.36 (KHTML, like Gecko) "
                  "Chrome/124.0.0.0 Safari/537.36",
}

cookies = {
    "session-id": "145-1234567-6543210",
    "i18n-prefs": "USD",
    "lc-main": "en_US",
    "sp-cdn": "L5Z9:EG",
}
# =========================================

def get_amazon_data_books(num_books, **kwargs):
    base_url = "https://www.amazon.com/s?k=data+engineering+books"
    url = f"{base_url}&page=1"
    time.sleep(2)
    response = requests.get(url, headers=headers, cookies=cookies, timeout=20)

    if response.status_code != 200:
        raise Exception(f"Failed to retrieve page, status {response.status_code}")

    soup = BeautifulSoup(response.content, "html.parser")
    book_containers = soup.find_all('div', {'data-component-type': 's-search-result'})
    if not book_containers:
        print("⚠️ No book containers found. Maybe Captcha page returned.")
        print(response.text[:1000])
        return []

    books = []
    for book in book_containers:
        title_tag = book.find('h2')
        title = title_tag.get_text(strip=True) if title_tag else None
        author_tag = book.find('div', class_='a-row a-size-base a-color-secondary')
        author = author_tag.get_text(strip=True).replace('by', '') if author_tag else None
        rating_tag = book.find('span', class_='a-icon-alt')
        rating = rating_tag.get_text(strip=True) if rating_tag else None

        if title:
            books.append({
                "Title": title,
                "Author": author,
                "Rating": rating,
            })

    books = books[:num_books]
    unique_books = {book['Title']: book for book in books}.values()
    return list(unique_books)

def insert_book_data_into_mysql(ti, **kwargs):
    book_data = ti.xcom_pull(task_ids='fetch_book_data')
    if not book_data:
        raise ValueError("No book data found in XCom.")

    mysql_hook = MySqlHook(mysql_conn_id='books_mysql_connection')
    insert_query = """
    INSERT INTO books (title, authors, rating)
    VALUES (%s, %s, %s)
    """
    for book in book_data:
        rating_str = book.get('Rating', '')
        rating = None
        if rating_str:
            try:
                rating = float(rating_str.split()[0])
            except:
                rating = None
        mysql_hook.run(insert_query, parameters=(book['Title'], book.get('Author'), rating))

def create_mysql_table():
    create_table_sql = """
    CREATE TABLE IF NOT EXISTS books (
        id INT AUTO_INCREMENT PRIMARY KEY,
        title VARCHAR(255) NOT NULL,
        authors VARCHAR(255),
        rating FLOAT
    );
    """
    mysql_hook = MySqlHook(mysql_conn_id='books_mysql_connection')
    mysql_hook.run(create_table_sql)

default_args = {
    'owner': 'airflow',
    'depends_on_past': False,
    'start_date': datetime(2025, 1, 1),
}

dag = DAG(
    'fetch_and_store_amazon_books',
    default_args=default_args,
    description='Fetch Amazon book data and store in MySQL',
    schedule_interval=timedelta(days=1),
    catchup=False,
)

create_table_task = PythonOperator(
    task_id='create_table',
    python_callable=create_mysql_table,
    dag=dag,
)

fetch_book_data_task = PythonOperator(
    task_id='fetch_book_data',
    python_callable=get_amazon_data_books,
    op_args=[50],
    dag=dag,
)

insert_book_data_task = PythonOperator(
    task_id='insert_book_data',
    python_callable=insert_book_data_into_mysql,
    dag=dag,
)

# -----------------------------
# Email notifications زي أول DAG
# -----------------------------
success_email = EmailOperator(
    task_id="send_success_email",
    to=["rwannada222@gmail.com"],
    subject="✅ Pipeline Succeeded",
    html_content="<h3>The pipeline has completed successfully 🎉</h3>",
    trigger_rule="all_success",
)

failure_email = EmailOperator(
    task_id="send_failure_email",
    to=["rwannada222@gmail.com"],
    subject="❌ Pipeline Failed",
    html_content="<h3>The pipeline has failed 🚨</h3>",
    trigger_rule="one_failed",
)

# ترتيب المهام مع الـ Email
create_table_task >> fetch_book_data_task >> insert_book_data_task >> [success_email, failure_email]
