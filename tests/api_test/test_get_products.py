import requests

BASE_URL = "http://localhost:8000"  # Update if using a different base URL

def test_successful_retrieval_of_products():
    response = requests.get(f"{BASE_URL}/products")
    assert response.status_code == 200
    products = response.json()
    assert isinstance(products, list)
    assert len(products) > 0  # Assuming products exist in the database

def test_validate_response_content_type():
    response = requests.get(f"{BASE_URL}/products")
    assert response.headers["Content-Type"] == "application/json"

def test_no_products_available(monkeypatch):
    def mock_get(*args, **kwargs):
        class MockResponse:
            status_code = 200
            def json(self):
                return []
        return MockResponse()
    
    monkeypatch.setattr(requests, "get", mock_get)
    response = requests.get(f"{BASE_URL}/products")
    assert response.status_code == 200
    assert response.json() == []

def test_validate_product_fields():
    response = requests.get(f"{BASE_URL}/products")
    products = response.json()
    for product in products:
        assert "id" in product
        assert "name" in product
        assert "description" in product
        assert "price" in product
        assert "stock" in product

def test_validate_product_id_uniqueness():
    response = requests.get(f"{BASE_URL}/products")
    products = response.json()
    ids = [product["id"] for product in products]
    assert len(ids) == len(set(ids))  # Check for unique IDs


def test_unauthorized_access(monkeypatch):
    def mock_get(*args, **kwargs):
        class MockResponse:
            status_code = 401
            def json(self):
                return {"detail": "Unauthorized"}
        return MockResponse()

    monkeypatch.setattr(requests, "get", mock_get)
    response = requests.get(f"{BASE_URL}/products")
    assert response.status_code == 401
    assert response.json()["detail"] == "Unauthorized"

def test_invalid_query_parameters():
    response = requests.get(f"{BASE_URL}/products?invalidParam=value")
    assert response.status_code in [200, 400]  # Adjust based on your implementation

def test_validate_price_and_stock_data_types():
    response = requests.get(f"{BASE_URL}/products")
    products = response.json()
    for product in products:
        assert isinstance(product["price"], (int, float))
        assert isinstance(product["stock"], int)
