import logging
import time
from extract import psycopg2_connection, extract_data
from settings import Settings
from load import upload_to_elastic
from state_storage import JsonFileStorage, State
from transform import transform_data
from init_elastic_search_index import initialize_elastic


def main() -> None:
    settings = Settings()
    state_storage = JsonFileStorage(settings.state_file_path)
    state = State(state_storage)
    initialize_elastic()
    pg_conn = psycopg2_connection()
    while True:
        results, last_modified = extract_data(pg_conn, state)
        data = transform_data(results)
        if data:
            upload_to_elastic(data)
            state.set_state('last_modified', last_modified)
            logging.warning(f"данные успешно загружены в elastic search: {len(data)} штук")
        time.sleep(settings.delay)


if __name__ == '__main__':
    main()
