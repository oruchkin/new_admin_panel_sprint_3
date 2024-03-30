from typing import List, Dict, Any
from elasticsearch import Elasticsearch, helpers
from settings import Settings


def upload_to_elastic(data: List[Dict[str, Any]]) -> None:
    settings = Settings()
    es_client = Elasticsearch([{'host': settings.elastic_host,
                                'port': settings.elastic_port,
                                'scheme': 'http'}])
    actions: List[Dict[str, Any]] = [
        {
            "_index": settings.elastic_index_name,
            "_id": item['id'],
            "_source": item
        }
        for item in data
    ]

    if actions:
        helpers.bulk(es_client, actions)
