import os
import redis
import json
from typing import Any
from app.frameworks.db.cache_strategy import CacheStrategy

class RedisCache(CacheStrategy):
    def __init__(self):
        host = os.getenv('REDIS_HOST')
        port = int(os.getenv('REDIS_PORT'))
        db = int(os.getenv('REDIS_DB'))

        self.client = redis.StrictRedis(host=host, port=port, db=db, decode_responses=True)

    def _serialize(self, value: Any) -> str:
        return json.dumps(value)

    def _deserialize(self, value: str) -> Any:
        return json.loads(value)

    def get(self, key: str) -> Any:
        value = self.client.get(key)
        if value is not None:
            return self._deserialize(value)
        return None

    def set(self, key: str, value: Any):
        serialized_value = self._serialize(value)
        self.client.set(key, serialized_value)

    def exists(self, key: str) -> bool:
        return self.client.exists(key)
