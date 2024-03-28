from settings import ConfigSettings

import psycopg2
from psycopg2.extras import DictCursor
from load_from_postgres import load_from_postgres
import time


def psycopg2_connection():
    dsl = {
        'dbname': conf_settings.pg_dbname,
        'user': conf_settings.pg_user,
        'password': conf_settings.pg_password,
        'host': conf_settings.pg_host,
        'port': conf_settings.pg_port
    }
    with psycopg2.connect(**dsl, cursor_factory=DictCursor) as pg_conn:
        return pg_conn



if __name__ == '__main__':
    conf_settings = ConfigSettings()



    while True:
        load_from_postgres(psycopg2_connection(), conf_settings.initial_date)
        time.sleep(5)
