from src.model import Product, Order
from src.schema import ProductSchema
from src.exception import OrderValidationError,ProductNameDuplicateError


class ProductService:
    def __init__(self):
        pass

    def get_all_products(self, SESSION):
        products = SESSION.query(Product).all()
        return ProductSchema(many=True).dump(products)

    def create_product(self, SESSION, name, description, price, stock):
        
        existing_product = SESSION.query(Product).filter(Product.name == name).first()
        if existing_product:
            raise ProductNameDuplicateError("Product with same name already exists")
        new_product = Product(
            name=name, description=description, price=price, stock=stock
        )
        SESSION.add(new_product)
        SESSION.commit()
        return ProductSchema().dump(new_product)

    def get_products_by_ids(self, SESSION, product_ids):
        products = SESSION.query(Product).filter(Product.id.in_(product_ids)).all()
        return products


class OrderService:
    def __init__(self):
        pass

    def create_order(self, SESSION, status, products):
        product_ids = [product.product_id for product in products]
        products_data = ProductService().get_products_by_ids(SESSION, product_ids)
        products_data_map = {product.id: product for product in products_data}
        out_of_stock_products = []
        total_price = 0
        for product in products:
            if product.product_id not in products_data_map:
                raise OrderValidationError(f"Product {product.product_id} not found")
            current_product=products_data_map[product.product_id]
            if product.quantity > current_product.stock:
                out_of_stock_products.append(product.product_id)
            else:
                total_price += product.quantity * current_product.price
                current_product.stock -= product.quantity
                SESSION.add(current_product)
        if len(out_of_stock_products) > 0:
            raise OrderValidationError(
                f"Products {out_of_stock_products} are out of stock"
            )
        _products=[{"product_id":product.product_id,"quantity":product.quantity} for product in products]
        new_order = Order(status=status, products=_products, total_price=total_price)
        SESSION.add(new_order)
        SESSION.commit()
        return True
