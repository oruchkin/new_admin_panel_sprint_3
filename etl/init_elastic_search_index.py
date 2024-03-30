import logging

from elasticsearch import Elasticsearch
from settings import Settings


def initialize_elastic() -> None:
    settings = Settings()
    es_client = Elasticsearch([{'host': settings.elastic_host,
                                'port': settings.elastic_port,
                                'scheme': 'http'}])
    index_settings = {
        "settings": {
            "refresh_interval": "1s",
            "analysis": {
                "filter": {
                    "english_stop": {
                        "type": "stop",
                        "stopwords": "_english_"
                    },
                    "english_stemmer": {
                        "type": "stemmer",
                        "language": "english"
                    },
                    "english_possessive_stemmer": {
                        "type": "stemmer",
                        "language": "possessive_english"
                    },
                    "russian_stop": {
                        "type": "stop",
                        "stopwords": "_russian_"
                    },
                    "russian_stemmer": {
                        "type": "stemmer",
                        "language": "russian"
                    }
                },
                "analyzer": {
                    "ru_en": {
                        "tokenizer": "standard",
                        "filter": [
                            "lowercase",
                            "english_stop",
                            "english_stemmer",
                            "english_possessive_stemmer",
                            "russian_stop",
                            "russian_stemmer"
                        ]
                    }
                }
            }
        },
        "mappings": {
            "dynamic": "strict",
            "properties": {
                "id": {"type": "keyword"},
                "imdb_rating": {"type": "float"},
                "genres": {"type": "keyword"},
                "title": {
                    "type": "text",
                    "analyzer": "ru_en",
                    "fields": {"raw": {"type": "keyword"}}
                },
                "description": {"type": "text", "analyzer": "ru_en"},
                "directors_names": {"type": "text", "analyzer": "ru_en"},
                "actors_names": {"type": "text", "analyzer": "ru_en"},
                "writers_names": {"type": "text", "analyzer": "ru_en"},
                "directors": {
                    "type": "nested",
                    "dynamic": "strict",
                    "properties": {
                        "id": {"type": "keyword"},
                        "name": {"type": "text", "analyzer": "ru_en"}
                    }
                },
                "actors": {
                    "type": "nested",
                    "dynamic": "strict",
                    "properties": {
                        "id": {"type": "keyword"},
                        "name": {"type": "text", "analyzer": "ru_en"}
                    }
                },
                "writers": {
                    "type": "nested",
                    "dynamic": "strict",
                    "properties": {
                        "id": {"type": "keyword"},
                        "name": {"type": "text", "analyzer": "ru_en"}
                    }
                }
            }
        }
    }
    index = settings.elastic_index_name
    if not es_client.indices.exists(index=index):
        logging.warning(f"создан индекс в elastic search {index}")
        es_client.indices.create(index=index, body=index_settings)
