from elasticsearch import Elasticsearch, helpers
from etl.settings import Settings


def upload_to_elastic(data):
    settings = Settings()
    es_client = Elasticsearch([{'host': settings.elastic_host,
                                'port': settings.elastic_port,
                                'scheme': 'http'}])
    actions = [
        {
            "_index": settings.elastic_index_name,
            "_id": item['id'],
            "_source": item
        }
        for item in data
    ]

    if actions:
        helpers.bulk(es_client, actions)
