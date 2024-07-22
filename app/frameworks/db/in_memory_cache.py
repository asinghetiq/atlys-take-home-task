from typing import Any
from app.frameworks.db.cache_strategy import CacheStrategy

class InMemoryCache(CacheStrategy):
    def __init__(self):
        self.cache = {}

    def get(self, key: str) -> Any:
        return self.cache.get(key)

    def set(self, key: str, value: Any):
        self.cache[key] = value

    def exists(self, key: str) -> bool:
        return key in self.cache
