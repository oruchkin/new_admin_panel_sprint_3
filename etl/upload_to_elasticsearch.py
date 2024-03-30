from elasticsearch import Elasticsearch, helpers
from settings import Settings
import json


def upload_to_elastic(data):
    print(data[0])
    print("------------------------upload_to_elastic------------------------")
    print(len(data))
    print(type(data))
    settings = Settings()
    es_client = Elasticsearch([{'host': settings.elastic_host, 'port': settings.elastic_port, 'scheme': 'http'}])
    actions = [
        {
            "_index": settings.elastic_index_name,
            "_id": item['id'],
            "_source": item
        }
        for item in data
    ]

    if actions:
        try:
            helpers.bulk(es_client, actions)
        except Exception as e:
            print(f"Ошибка при индексации документов: {e}")
