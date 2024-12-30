from marshmallow_sqlalchemy import SQLAlchemyAutoSchema
from .model import Product


class ProductSchema(SQLAlchemyAutoSchema):
    class Meta:
        model = Product
        load_instance = True