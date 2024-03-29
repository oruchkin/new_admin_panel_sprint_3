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


def fetch_data(pg_conn):
    with pg_conn.cursor() as cursor:
        cursor.execute("""
            SELECT fw.id, 
                   fw.title, 
                   fw.description, 
                   fw.rating, 
                   array_agg(DISTINCT g.name) AS genres,
                   array_agg(DISTINCT jsonb_build_object('id', p.id, 'name', p.full_name)) FILTER (WHERE pfw.role = 'director') AS directors,
                   array_agg(DISTINCT jsonb_build_object('id', p.id, 'name', p.full_name)) FILTER (WHERE pfw.role = 'actor') AS actors,
                   array_agg(DISTINCT jsonb_build_object('id', p.id, 'name', p.full_name)) FILTER (WHERE pfw.role = 'writer') AS writers
            FROM content.film_work fw
            LEFT JOIN content.genre_film_work gfw ON fw.id = gfw.film_work_id
            LEFT JOIN content.genre g ON gfw.genre_id = g.id
            LEFT JOIN content.person_film_work pfw ON fw.id = pfw.film_work_id
            LEFT JOIN content.person p ON pfw.person_id = p.id
            GROUP BY fw.id
            LIMIT 1000000000;
        """)
        results = cursor.fetchall()
        # Преобразование результатов в структуру, подходящую для класса Movie
        data = []
        for row in results:
            movie_data = {
                "id": row["id"],
                "title": row["title"],
                "description": row["description"],
                "rating": row["rating"],
                "genres": row["genres"],
                "directors": row["directors"] if row.get("directors") else [],
                "actors": row["actors"] if row.get("actors") else [],
                "writers": row["writers"] if row.get("writers") else []
            }
            data.append(movie_data)
        return data
