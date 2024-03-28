from psycopg2.extensions import connection as _connection




def load_from_postgres(pg_conn: _connection, initial_date: str):
    # TODO: здесь будет загрузка из постгреса
    # так же здесь должен быть JsonFileStorage в котором будет храниться состояние

