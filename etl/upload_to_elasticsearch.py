from elasticsearch import Elasticsearch, helpers
from settings import Settings
import json


class Movie:
    def __init__(self, movie_id, title, description, rating, genres, directors=[], actors=[], writers=[]):
        self.id = movie_id
        self.title = title
        self.description = description
        self.imdb_rating = rating
        self.genres = genres
        self.directors = directors
        self.actors = actors
        self.writers = writers
        self.directors_names = [director['name'] for director in directors]
        self.actors_names = [actor['name'] for actor in actors]
        self.writers_names = [writer['name'] for writer in writers]

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



def upload_to_elastic(data):
    print(data)
    print("------------------------")
    print(len(data))
    print(type(data))
    settings = Settings()
    es_client = Elasticsearch([{'host': settings.elastic_host, 'port': settings.elastic_port, 'scheme': 'http'}])

    actions = []
    for item in data:
        movie = Movie(item["id"], item["title"], item["description"], item["rating"], item["genres"], item.get("directors", []), item.get("actors", []), item.get("writers", []))
        movie_dict = movie.to_dict()
        action = {
            "_index": settings.elastic_index_name,
            "_id": movie_dict['id'],
            "_source": movie_dict
        }
        actions.append(action)

    if actions:
        # TODO: сделать эту штуку безотказной в случае если не загружается то что-то делать
        try:
            helpers.bulk(es_client, actions)
            print("после балка")
        except Exception as e:
            print(f"Ошибка при индексации документов: {e}")
