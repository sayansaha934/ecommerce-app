import pytest
from unittest.mock import MagicMock
import os, sys
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../../')))
from src.service import OrderService
from src.model import Order,Product
from src.exception import OrderValidationError

@pytest.fixture
def mock_session():
    # Mock the session to simulate database interaction
    return MagicMock()

@pytest.fixture
def mock_product_service(mocker):
    # Mock the ProductService to simulate product-related operations
    return mocker.patch("src.service.ProductService")

@pytest.fixture
def sample_products():
    # Sample input products for an order
    class InputProduct:
        def __init__(self, product_id, quantity):
            self.product_id = product_id
            self.quantity = quantity

    return [
        InputProduct(product_id=1, quantity=2),
        InputProduct(product_id=2, quantity=1),
    ]

@pytest.fixture
def database_products():
    # Sample products in the database
    return [
        Product(id=1, name="Product 1", price=50.0, stock=5),
        Product(id=2, name="Product 2", price=30.0, stock=2),
    ]

def test_create_order_success(mock_session, mock_product_service, sample_products, database_products):
    """
    Test case for successfully creating an order.
    """
    # Mock ProductService to return the products from the database
    mock_product_service.return_value.get_products_by_ids.return_value = database_products

    # Initialize OrderService
    service = OrderService()

    # Call the method
    result = service.create_order(mock_session, status="Pending", products=sample_products)

    # Assertions
    assert result is True
    mock_product_service.return_value.get_products_by_ids.assert_called_once_with(
        mock_session, [1, 2]
    )

    # Ensure that the database products' stock is updated
    assert database_products[0].stock == 3  # Reduced by 2
    assert database_products[1].stock == 1  # Reduced by 1

    # Verify that the new order is added to the session
    added_order = mock_session.add.call_args[0][0]
    assert isinstance(added_order, Order)
    assert added_order.status == "Pending"
    assert added_order.total_price == 130.0  # (2 * 50) + (1 * 30)
    assert added_order.products == [{"product_id": 1, "quantity": 2}, {"product_id": 2, "quantity": 1}]

    # Ensure the session was committed
    mock_session.commit.assert_called_once()


def test_create_order_product_not_found_failure(mock_session, mock_product_service, sample_products):
    """
    Test case for failure when a product ID is not found in the database.
    """
    # Mock ProductService to return only one product (missing product ID 2)
    mock_product_service.return_value.get_products_by_ids.return_value = [
        Product(id=1, name="Product 1", price=50.0, stock=5)
    ]

    # Initialize OrderService
    service = OrderService()

    # Call the method and expect an exception
    with pytest.raises(OrderValidationError) as excinfo:
        service.create_order(mock_session, status="Pending", products=sample_products)

    # Assertions
    assert str(excinfo.value) == "Product 2 not found"
    mock_product_service.return_value.get_products_by_ids.assert_called_once_with(
        mock_session, [1, 2]
    )


def test_create_order_out_of_stock_failure(mock_session, mock_product_service, sample_products, database_products):
    """
    Test case for failure when a product is out of stock.
    """
    # Reduce the stock of one product to cause an out-of-stock error
    database_products[1].stock = 0  # Product ID 2 is out of stock

    # Mock ProductService to return the products from the database
    mock_product_service.return_value.get_products_by_ids.return_value = database_products

    # Initialize OrderService
    service = OrderService()

    # Call the method and expect an exception
    with pytest.raises(OrderValidationError) as excinfo:
        service.create_order(mock_session, status="Pending", products=sample_products)

    # Assertions
    assert str(excinfo.value) == "Products [2] are out of stock"
    mock_product_service.return_value.get_products_by_ids.assert_called_once_with(
        mock_session, [1, 2]
    )
