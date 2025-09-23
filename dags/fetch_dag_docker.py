from datetime import datetime, timedelta
from airflow import DAG
import requests
import pandas as pd
from bs4 import BeautifulSoup
from airflow.operators.python import PythonOperator
from airflow.providers.mysql.hooks.mysql import MySqlHook

headers = {
    "Referer": "https://www.amazon.com/",
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/117.0.0.0 Safari/537.36",
    "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8",
    "Accept-Encoding": "gzip, deflate, br",
    "Accept-Language": "en-US,en;q=0.9",
    "Connection": "keep-alive",
    "Upgrade-Insecure-Requests": "1"
}

def get_amazon_data_books(num_books, **kwargs):
    base_url = f"https://www.amazon.com/s?k=data+engineering+books"
    books = []
    page = 1
    url = f"{base_url}&page={page}"
    response = requests.get(url, headers=headers)
    
    if response.status_code == 200:
        soup = BeautifulSoup(response.content, "html.parser")
        book_containers = soup.find_all('div', {'data-component-type': 's-search-result'})
        for book in book_containers:
            title_tag = book.find('h2')
            title = title_tag.get_text(strip=True) if title_tag else None
            author_tag = book.find('div', class_='a-row a-size-base a-color-secondary')
            author = author_tag.get_text(strip=True).replace('by', '') if author_tag else None
            rating_tag = book.find('span', class_='a-icon-alt')
            rating = rating_tag.get_text(strip=True) if rating_tag else None
            
            books.append({
                "Title": title,
                "Author": author,
                "Rating": rating,
            })
    else:
        raise Exception("Failed to retrieve the page")
    
    books = books[:num_books]
    # Remove duplicates
    unique_books = {book['Title']: book for book in books}.values()
    unique_books_list = list(unique_books)
    
    print(f"Fetched {len(unique_books_list)} unique books")
    
    # Push list of dicts to XCom
    return unique_books_list
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
        # Clean rating (e.g. "4.5 out of 5 stars" -> 4.5)
        rating_str = book.get('Rating', '')
        rating = None
        if rating_str:
            try:
                rating = float(rating_str.split()[0])
            except:
                rating = None

        mysql_hook.run(insert_query, parameters=(
            book['Title'], book['Author'], rating
        ))

def create_mysql_table():
    create_table_sql = """
    CREATE TABLE IF NOT EXISTS books (
        id INT AUTO_INCREMENT PRIMARY KEY,
        title VARCHAR(255) NOT NULL,
        authors VARCHAR(255),
        price VARCHAR(50),
        rating VARCHAR(50)
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
    description='A DAG to fetch book data from Amazon and store it in MySQL',
    schedule_interval=timedelta(days=1),
    catchup=False,)

fetch_book_data_task = PythonOperator(
    task_id='fetch_book_data',
    python_callable=get_amazon_data_books,
    op_args=[50],  # Number of books
    dag=dag,
)

insert_book_data_task = PythonOperator(
    task_id='insert_book_data',
    python_callable=insert_book_data_into_mysql,
    dag=dag,
)

create_table_task = PythonOperator(
    task_id='create_table',
    python_callable=create_mysql_table,
    dag=dag,
)

fetch_book_data_task >> create_table_task >> insert_book_data_task
