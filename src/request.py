from pydantic import BaseModel, HttpUrl
from typing import List
from enum import Enum

from pydantic import BaseModel, root_validator, ValidationError

class CreateProductRequest(BaseModel):
    name: str
    description: str
    price: float
    stock: int

    @root_validator(pre=True)
    def check_non_negative(cls, values):
        price = values.get('price')
        stock = values.get('stock')
        
        if price is not None and price < 0:
            raise ValueError('Price cannot be negative')
        if stock is not None and stock < 0:
            raise ValueError('Stock cannot be negative')
        
        return values



class Products(BaseModel):
    product_id: int
    quantity: int
    @root_validator(pre=True)
    def check_non_negative(cls, values):
        quantity = values.get('quantity')
        
        
        if quantity is not None and quantity < 0:
            raise ValueError('Quantity cannot be negative')
        
        
        return values
class Status(Enum):
    pending = "pending"
    completed = "completed"

class CreateOrderRequest(BaseModel):
    status: Status
    products: List[Products]
    @root_validator(pre=True)
    def check_products(cls, values):
        products = values.get('products', [])
        if not products:
            raise ValueError('There must be at least one product in the order')
        return values
