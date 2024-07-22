import json
import os
from typing import List
from app.adapters.storage_adapter import StorageHandler
from app.core.entities.product import Product
from app.frameworks.db.cache_strategy import CacheStrategy

class JSONStorageHandler(StorageHandler):
    def __init__(self, cache: CacheStrategy):
        self.cache = cache

    def save(self, data: List[Product]):
        file_path = 'products.json'
        if os.path.exists(file_path):
            with open(file_path, 'r') as file:
                existing_data = json.load(file)
        else:
            existing_data = []

        existing_titles = {product['product_title'] for product in existing_data}

        for product in data:
            product_dict = product.dict()
            product_title = product_dict['product_title']
            product_price = product_dict['product_price']

            cached_price = self.cache.get(product_title)
            if cached_price and cached_price == product_price:
                continue

            self.cache.set(product_title, product_price)
            if product_title in existing_titles:
                for item in existing_data:
                    if item['product_title'] == product_title:
                        item['product_price'] = product_price
            else:
                existing_data.append(product_dict)

        with open(file_path, 'w') as file:
            json.dump(existing_data, file, indent=4)
