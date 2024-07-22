from abc import ABC, abstractmethod
from typing import List
from app.core.entities.product import Product

class StorageHandler(ABC):
    @abstractmethod
    def save(self, data: List[Product]):
        pass
