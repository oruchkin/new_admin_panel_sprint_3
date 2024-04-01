from typing import Any, Dict, List

from elasticsearch import Elasticsearch, helpers

from decorators import backoff
from settings import Settings


@backoff()
def upload_to_elastic(data: List[Dict[str, Any]],
                      es_client: Elasticsearch) -> None:
    settings = Settings()
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
