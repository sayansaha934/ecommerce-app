import requests
import random
import string

BASE_URL = "http://localhost:8000"  # Update if using a different base URL
def generate_random_name(length=10):
    return ''.join(random.choices(string.ascii_letters + string.digits, k=length))

def test_successful_product_creation():
    random_name = generate_random_name()

    payload = {
        "name": random_name,
        "description": "Test",
        "price": 100,
        "stock": 50
    }
    response = requests.post(f"{BASE_URL}/products", json=payload)
    assert response.status_code == 200
    product = response.json()
    assert product["id"] is not None
    assert product["name"] == payload["name"]
    assert product["description"] == payload["description"]
    assert product["price"] == payload["price"]
    assert product["stock"] == payload["stock"]

def test_missing_required_fields():
    payload = {
        "name": "Rug 67GSM"
    }
    response = requests.post(f"{BASE_URL}/products", json=payload)
    assert response.status_code == 422
    

def test_invalid_data_types():
    payload = {
        "name": "Rug 67GSM",
        "description": "Premium gsm",
        "price": "one hundred",
        "stock": "fifty"
    }
    response = requests.post(f"{BASE_URL}/products", json=payload)
    assert response.status_code == 422
    
    

def test_negative_values_for_price_and_stock():
    payload = {
        "name": "Rug 67GSM",
        "description": "Premium gsm",
        "price": -100,
        "stock": -50
    }
    response = requests.post(f"{BASE_URL}/products", json=payload)
    assert response.status_code == 422
    
    

def test_duplicate_product_name(monkeypatch):
    payload = {
        "name": "Rug 67GSM",
        "description": "Premium gsm",
        "price": 100,
        "stock": 50
    }

    def mock_post(*args, **kwargs):
        class MockResponse:
            status_code = 409
            def json(self):
                return {"error": "Duplicate product name"}
        return MockResponse()

    monkeypatch.setattr(requests, "post", mock_post)
    response = requests.post(f"{BASE_URL}/products", json=payload)
    assert response.status_code == 409



def test_unauthorized_access(monkeypatch):
    payload = {
        "name": "Rug 67GSM",
        "description": "Premium gsm",
        "price": 100,
        "stock": 50
    }

    def mock_post(*args, **kwargs):
        class MockResponse:
            status_code = 401
            def json(self):
                return {"error": "Unauthorized"}
        return MockResponse()

    monkeypatch.setattr(requests, "post", mock_post)
    response = requests.post(f"{BASE_URL}/products", json=payload)
    assert response.status_code == 401
    error = response.json()
    assert "error" in error
    assert error["error"] == "Unauthorized"

def test_valid_product_with_edge_values():
    random_name = generate_random_name()
    payload = {
        "name": random_name,
        "description": "Testing edge values",
        "price": 0,
        "stock": 0
    }
    response = requests.post(f"{BASE_URL}/products", json=payload)
    assert response.status_code == 200
    product = response.json()
    assert product["id"] is not None
    assert product["name"] == payload["name"]
    assert product["description"] == payload["description"]
    assert product["price"] == payload["price"]
    assert product["stock"] == payload["stock"]


