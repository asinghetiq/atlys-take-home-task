from typing import Any
from abc import ABC, abstractmethod

class CacheStrategy(ABC):
    @abstractmethod
    def get(self, key: str) -> Any:
        pass

    @abstractmethod
    def set(self, key: str, value: Any):
        pass

    @abstractmethod
    def exists(self, key: str) -> bool:
        pass
