import time
from settings import Settings
from load_from_postgres import psycopg2_connection, fetch_data
from upload_to_elasticsearch import upload_to_elastic
from state_storage import JsonFileStorage, State


def main():
    settings = Settings()
    state_storage = JsonFileStorage(settings.state_file_path)
    state = State(state_storage)
    print("11123")
    print(settings.state_file_path)
    print(state)

    pg_conn = psycopg2_connection()
    while True:
        data, last_modified = fetch_data(pg_conn, state)
        print("in main")
        print(last_modified)
        if data:
            upload_to_elastic(data)
            state.set_state('last_modified', last_modified)
        time.sleep(settings.delay)

if __name__ == '__main__':
    main()
