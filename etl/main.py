import time
from settings import Settings
from etl_scripts.extract import psycopg2_connection, extract_data
from etl_scripts.load import upload_to_elastic
from etl_scripts.state_storage import JsonFileStorage, State

from etl_scripts.transform import transform_data



def main():
    settings = Settings()
    state_storage = JsonFileStorage(settings.state_file_path)
    state = State(state_storage)


    pg_conn = psycopg2_connection()
    while True:
        results, last_modified = extract_data(pg_conn, state)
        data = transform_data(results)
        print("in main")
        print(last_modified)
        if data:
            upload_to_elastic(data)
            state.set_state('last_modified', last_modified)
        time.sleep(settings.delay)

if __name__ == '__main__':
    main()
