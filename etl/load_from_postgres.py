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

class Movie:
    def __init__(self, movie_id, title, description, rating, genres, directors=None, actors=None, writers=None):
        self.id = movie_id
        self.title = title
        self.description = description
        self.imdb_rating = rating
        self.genres = genres
        self.directors = directors if directors is not None else []
        self.actors = actors if actors is not None else []
        self.writers = writers if writers is not None else []
        self.directors_names = [director['name'] for director in self.directors]
        self.actors_names = [actor['name'] for actor in self.actors]
        self.writers_names = [writer['name'] for writer in self.writers]

    def to_dict(self):
        return {
            "id": self.id,
            "title": self.title,
            "description": self.description,
            "imdb_rating": self.imdb_rating,
            "genres": self.genres,
            "directors": self.directors,
            "actors": self.actors,
            "writers": self.writers,
            "directors_names": self.directors_names,
            "actors_names": self.actors_names,
            "writers_names": self.writers_names
        }


def transform_data(results):
    """Преобразование результатов запроса в список экземпляров класса Movie."""
    movies = []
    for row in results:
        movie = Movie(
            movie_id=row['id'],
            title=row['title'],
            description=row['description'],
            rating=row['rating'],
            genres=row['genres'],
            directors=row['directors'],
            actors=row['actors'],
            writers=row['writers']
        )
        movies.append(movie.to_dict())  # Преобразование экземпляра класса Movie в словарь
    return movies

def fetch_data(pg_conn, state):
    last_modified = state.get_state('last_modified') or '1970-01-01'
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
        if results:
            last_modified = results[0]['last_modified'].strftime('%Y-%m-%dT%H:%M:%S.%f')[:-3] + 'Z'
        data = transform_data(results)  # Использование метода transform_data для преобразования данных
    return data, last_modified

#
# def fetch_data(pg_conn, state):
#     last_modified = state.get_state('last_modified') or '1970-01-01'
#     print("00009999---- fetchdata")
#     print(last_modified)
#     with pg_conn.cursor() as cursor:
#         cursor.execute("""
#             SELECT fw.id,
#                    fw.title,
#                    fw.description,
#                    fw.rating,
#                    array_agg(DISTINCT g.name) AS genres,
#                    array_agg(DISTINCT jsonb_build_object('id', p.id, 'name', p.full_name)) FILTER (WHERE pfw.role = 'director') AS directors,
#                    array_agg(DISTINCT jsonb_build_object('id', p.id, 'name', p.full_name)) FILTER (WHERE pfw.role = 'actor') AS actors,
#                    array_agg(DISTINCT jsonb_build_object('id', p.id, 'name', p.full_name)) FILTER (WHERE pfw.role = 'writer') AS writers,
#                    MAX(GREATEST(fw.modified, g.modified, p.modified)) AS last_modified
#             FROM content.film_work fw
#             LEFT JOIN content.genre_film_work gfw ON fw.id = gfw.film_work_id
#             LEFT JOIN content.genre g ON gfw.genre_id = g.id
#             LEFT JOIN content.person_film_work pfw ON fw.id = pfw.film_work_id
#             LEFT JOIN content.person p ON pfw.person_id = p.id
#             WHERE fw.modified > %s OR g.modified > %s OR p.modified > %s
#             GROUP BY fw.id
#             ORDER BY last_modified DESC
#             LIMIT 1000;
#         """, (last_modified, last_modified, last_modified))
#         results = cursor.fetchall()
#         print("len(results)")
#         print(results)
#         print(len(results))
#
#         if results:
#             last_modified = results[0]['last_modified'] # Преобразование datetime в строку с миллисекундами
#             print("last_modified")
#             print(last_modified)
#             # print("last_modified")
#             # print(last_modified)
#             #
#             # last_modified = results[0]['last_modified'].strftime('%Y-%m-%dT%H:%M:%S')  # Преобразование datetime в строку
#         data = [{'id': row['id'], 'title': row['title'], 'description': row['description'], 'rating': row['rating'], 'genres': row['genres'], 'directors': row['directors'], 'actors': row['actors'], 'writers': row['writers']} for row in results]
#     return data, last_modified
