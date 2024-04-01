import logging
import time

from elasticsearch import Elasticsearch

from extract import extract_data, psycopg2_connection
from init_elastic_search_index import initialize_elastic
from load import upload_to_elastic
from settings import Settings
from state_storage import JsonFileStorage, State
from transform import transform_data


def main() -> None:
    settings = Settings()
    state_storage = JsonFileStorage(settings.state_file_path)
    state = State(state_storage)
    initialize_elastic()
    pg_conn = psycopg2_connection()
    es_client = Elasticsearch([{'host': settings.elastic_host,
                                'port': settings.elastic_port,
                                'scheme': settings.elastic_port}])

    while True:
        for batch in extract_data(pg_conn, state, batch_size=300):
            if batch:
                last_record = batch[-1]
                last_modified = last_record['last_modified'] \
                                    .strftime('%Y-%m-%dT%H:%M:%S.%f')[:-3] + 'Z'

                transformed_batch = transform_data(batch)
                if transformed_batch:
                    upload_to_elastic(transformed_batch, es_client)
                    state.set_state('last_modified', last_modified)
                    logging.warning(
                        f"данные успешно загружены в elastic search: "
                        f"{len(transformed_batch)} штук"
                    )

        time.sleep(settings.delay)


if __name__ == '__main__':
    main()
