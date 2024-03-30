import psycopg2
from psycopg2.extras import DictCursor
from settings import Settings
from backoff import backoff

@backoff()
def psycopg2_connection():
    settings = Settings()
    dsl = {
        'dbname': settings.postgres_dbname,
        'user': settings.postgres_user,
        'password': settings.postgres_password,
        'host': settings.postgres_host,
        'port': settings.postgres_port
    }
    return psycopg2.connect(**dsl, cursor_factory=DictCursor)


def fetch_data(pg_conn, state):
    last_modified = state.get_state('last_modified') or '1970-01-01'
    print("00009999---- fetchdata")
    print(last_modified)
    with pg_conn.cursor() as cursor:
        cursor.execute("""
            SELECT fw.id, 
                   fw.title, 
                   fw.description, 
                   fw.rating, 
                   array_agg(DISTINCT g.name) AS genres,
                   array_agg(DISTINCT jsonb_build_object('id', p.id, 'name', p.full_name)) FILTER (WHERE pfw.role = 'director') AS directors,
                   array_agg(DISTINCT jsonb_build_object('id', p.id, 'name', p.full_name)) FILTER (WHERE pfw.role = 'actor') AS actors,
                   array_agg(DISTINCT jsonb_build_object('id', p.id, 'name', p.full_name)) FILTER (WHERE pfw.role = 'writer') AS writers,
                   MAX(GREATEST(fw.modified, g.modified, p.modified)) AS last_modified
            FROM content.film_work fw
            LEFT JOIN content.genre_film_work gfw ON fw.id = gfw.film_work_id
            LEFT JOIN content.genre g ON gfw.genre_id = g.id
            LEFT JOIN content.person_film_work pfw ON fw.id = pfw.film_work_id
            LEFT JOIN content.person p ON pfw.person_id = p.id
            WHERE fw.modified > %s OR g.modified > %s OR p.modified > %s
            GROUP BY fw.id
            ORDER BY last_modified DESC
            LIMIT 1000;
        """, (last_modified, last_modified, last_modified))
        results = cursor.fetchall()
        print("len(results)")
        print(results)
        print(len(results))

        if results:
            last_modified = results[0]['last_modified'] # Преобразование datetime в строку с миллисекундами
            print("last_modified")
            print(last_modified)
            # print("last_modified")
            # print(last_modified)
            #
            # last_modified = results[0]['last_modified'].strftime('%Y-%m-%dT%H:%M:%S')  # Преобразование datetime в строку
        data = [{'id': row['id'], 'title': row['title'], 'description': row['description'], 'rating': row['rating'], 'genres': row['genres'], 'directors': row['directors'], 'actors': row['actors'], 'writers': row['writers']} for row in results]
    return data, last_modified
