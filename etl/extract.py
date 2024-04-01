from typing import Any, Dict, Generator, List, Tuple

import psycopg2
from psycopg2.extensions import connection as PgConnection
from psycopg2.extras import DictCursor

from decorators import backoff
from settings import Settings


@backoff()
def psycopg2_connection() -> PgConnection:
    settings = Settings()
    dsl = {
        'dbname': settings.postgres_dbname,
        'user': settings.postgres_user,
        'password': settings.postgres_password,
        'host': settings.postgres_host,
        'port': settings.postgres_port
    }
    return psycopg2.connect(**dsl, cursor_factory=DictCursor)


def extract_data(pg_conn, state, batch_size=100) -> Generator[List[Dict[str, Any]], None, None]:
    last_modified = state.get_state('last_modified') or '1970-01-01'

    with pg_conn.cursor() as cursor:
        cursor.execute("""
            SELECT fw.id, 
                   fw.title, 
                   fw.description, 
                   fw.rating, 
                   array_agg(DISTINCT g.name) AS genres,
                   array_agg(DISTINCT jsonb_build_object('id', p.id, 'name', p.full_name)) 
                   FILTER (WHERE pfw.role = 'director') AS directors,
                   array_agg(DISTINCT jsonb_build_object('id', p.id, 'name', p.full_name)) 
                   FILTER (WHERE pfw.role = 'actor') AS actors,
                   array_agg(DISTINCT jsonb_build_object('id', p.id, 'name', p.full_name)) 
                   FILTER (WHERE pfw.role = 'writer') AS writers,
                   MAX(GREATEST(fw.modified, g.modified, p.modified)) AS last_modified
            FROM content.film_work fw
            LEFT JOIN content.genre_film_work gfw ON fw.id = gfw.film_work_id
            LEFT JOIN content.genre g ON gfw.genre_id = g.id
            LEFT JOIN content.person_film_work pfw ON fw.id = pfw.film_work_id
            LEFT JOIN content.person p ON pfw.person_id = p.id
            WHERE fw.modified > %s OR g.modified > %s OR p.modified > %s
            GROUP BY fw.id
            ORDER BY last_modified DESC;
        """, (last_modified, last_modified, last_modified))

        while True:
            batch = cursor.fetchmany(batch_size)
            if not batch:
                break
            yield batch
