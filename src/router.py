from fastapi import APIRouter
from fastapi.responses import JSONResponse
from src.service import ProductService, OrderService
from src.request import CreateProductRequest, CreateOrderRequest
from db import SESSION
from src.exception import OrderValidationError,ProductNameDuplicateError

router = APIRouter()


@router.get("/products")
def get_all_products():
    try:
        products = ProductService().get_all_products(SESSION=SESSION)
        SESSION.close()
        return JSONResponse(status_code=200, content=products)
    except Exception as e:
        print(e)
        SESSION.rollback()
        return JSONResponse(status_code=500, content=str(e))


@router.post("/products")
def create_product(args: CreateProductRequest):
    try:
        new_game = ProductService().create_product(
            SESSION=SESSION,
            name=args.name,
            description=args.description,
            price=args.price,
            stock=args.stock,
        )
        SESSION.close()
        return JSONResponse(status_code=200, content=new_game)
    except ProductNameDuplicateError as e:
        SESSION.rollback()
        return JSONResponse(status_code=409, content=str(e.message))
    except Exception as e:
        print(e)
        SESSION.rollback()
        return JSONResponse(status_code=500, content=str(e))


@router.post("/orders")
def create_order(args: CreateOrderRequest):
    try:
        OrderService().create_order(
            SESSION=SESSION, status=args.status.value, products=args.products
        )
        SESSION.close()
        return JSONResponse(status_code=200, content={"message": "Order created successfully"})
    except OrderValidationError as e:
        SESSION.rollback()
        return JSONResponse(status_code=409, content=str(e.message))
    except Exception as e:
        print(e)
        SESSION.rollback()
        return JSONResponse(status_code=500, content=str(e))
