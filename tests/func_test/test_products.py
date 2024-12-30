import pytest
from unittest.mock import MagicMock
import os, sys
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../../')))

from src.service import ProductService
from src.model import Product
from src.schema import ProductSchema 
from src.exception import ProductNameDuplicateError
@pytest.fixture
def mock_session():
    # Mock the session to simulate database interaction
    mock_session = MagicMock()
    return mock_session

@pytest.fixture
def sample_products():
    # Return a list of sample Product instances
    return [
        Product(name="Product 1", price=10.0),
        Product(name="Product 2", price=20.0),
    ]

def test_get_all_products(mock_session, sample_products):
    # Mock the query to return a predefined list of products
    mock_session.query.return_value.all.return_value = sample_products
    
    
    result = ProductService().get_all_products(mock_session)
    
    # Check if the result is as expected
    assert len(result) == 2  # The number of products
    assert result[0]["name"] == "Product 1"  # Check product name
    assert result[1]["price"] == 20.0  # Check product price
    
    # Ensure the session query method was called correctly
    mock_session.query.assert_called_once_with(Product)
    mock_session.query.return_value.all.assert_called_once()

def test_get_all_products_failure(mock_session):
    """
    Test case for failure when no products are returned.
    """
    # Mock the query to return an empty list
    mock_session.query.return_value.all.return_value = []

    result = ProductService().get_all_products(mock_session)

    # Assertions for failure case
    assert result == []  # Expecting an empty list
    mock_session.query.assert_called_once_with(Product)
    mock_session.query.return_value.all.assert_called_once()


def test_get_all_products_exception_handling(mock_session):
    """
    Test case for exception handling during database query.
    """
    # Mock the query to raise an exception
    mock_session.query.side_effect = Exception("Database connection error")

    # Use pytest to check if the exception is raised
    with pytest.raises(Exception) as excinfo:
        ProductService().get_all_products(mock_session)

    # Assertions for exception handling
    assert str(excinfo.value) == "Database connection error"
    mock_session.query.assert_called_once_with(Product)


@pytest.fixture
def sample_product():
    # Sample product data for testing
    return Product(
        name="Test Product",
        description="A sample product for testing",
        price=100.0,
        stock=50,
    )



def test_create_product_success(mock_session, sample_product):
    """
    Test case for successfully creating a new product.
    """
    service = ProductService()

    # Mock the query to simulate no existing product with the same name
    mock_session.query.return_value.filter.return_value.first.return_value = None

    # Mock adding and committing the product
    mock_session.add.return_value = None
    mock_session.commit.return_value = None

    # Call the method
    result = service.create_product(
        mock_session, sample_product.name, sample_product.description, sample_product.price, sample_product.stock
    )

    # Assertions
    assert result["name"] == sample_product.name
    assert result["description"] == sample_product.description
    assert result["price"] == sample_product.price
    assert result["stock"] == sample_product.stock

    # Use `ANY` to bypass instance comparison
    mock_session.add.assert_called_once()
    added_product = mock_session.add.call_args[0][0]  # Get the actual object passed to add
    assert added_product.name == sample_product.name
    assert added_product.description == sample_product.description
    assert added_product.price == sample_product.price
    assert added_product.stock == sample_product.stock
    mock_session.commit.assert_called_once()


def test_create_product_duplicate_name_failure(mock_session, sample_product):
    """
    Test case for failure when a product with the same name already exists.
    """
    service = ProductService()

    # Mock the query to simulate an existing product with the same name
    mock_session.query.return_value.filter.return_value.first.return_value = sample_product

    # Call the method and expect a ProductNameDuplicateError
    with pytest.raises(ProductNameDuplicateError) as excinfo:
        service.create_product(
            mock_session, sample_product.name, sample_product.description, sample_product.price, sample_product.stock
        )

    # Assertions
    assert str(excinfo.value) == "Product with same name already exists"

    # Ensure query was called and no product was added or committed
    mock_session.query.assert_called_once()
    mock_session.add.assert_not_called()
    mock_session.commit.assert_not_called()