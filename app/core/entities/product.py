from pydantic import BaseModel

class Product(BaseModel):
    product_title: str
    product_price: int
    path_to_image: str
