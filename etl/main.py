import time
from settings import Settings
from load_from_postgres import psycopg2_connection, fetch_data
from upload_to_elasticsearch import upload_to_elastic

def main():
    settings = Settings()
    pg_conn = psycopg2_connection()
    while True:
        data = fetch_data(pg_conn)
        if data:
            upload_to_elastic(data)
        time.sleep(settings.delay)

if __name__ == '__main__':
    main()
