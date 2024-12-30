import requests

BASE_URL = "http://localhost:8000"  # Update if using a different base URL

def test_successful_order_creation():
    payload = {
        "status": "pending",
        "products": [
            {"product_id": 1, "quantity": 1}
        ]
    }
    response = requests.post(f"{BASE_URL}/orders", json=payload)
    assert response.status_code == 200
    

def test_missing_required_fields():
    payload = {
        "status": "pending"
    }
    response = requests.post(f"{BASE_URL}/orders", json=payload)
    assert response.status_code == 422
    
    

def test_invalid_product_id():
    payload = {
        "status": "pending",
        "products": [
            {"product_id": 99999, "quantity": 1}
        ]
    }
    response = requests.post(f"{BASE_URL}/orders", json=payload)
    assert response.status_code == 409
    
    

def test_negative_quantity():
    payload = {
        "status": "pending",
        "products": [
            {"product_id": 1, "quantity": -1}
        ]
    }
    response = requests.post(f"{BASE_URL}/orders", json=payload)
    assert response.status_code == 422
    
def test_invalid_status():
    payload = {
        "status": "invalid_status",
        "products": [
            {"product_id": 1, "quantity": 1}
        ]
    }
    response = requests.post(f"{BASE_URL}/orders", json=payload)
    assert response.status_code == 422
   

def test_missing_product_in_order():
    payload = {
        "status": "pending",
        "products": []
    }
    response = requests.post(f"{BASE_URL}/orders", json=payload)
    assert response.status_code == 422
    
    

def test_unauthorized_access(monkeypatch):
    payload = {
        "status": "pending",
        "products": [
            {"product_id": 1, "quantity": 1}
        ]
    }

    def mock_post(*args, **kwargs):
        class MockResponse:
            status_code = 401
            def json(self):
                return {"error": "Unauthorized"}
        return MockResponse()

    monkeypatch.setattr(requests, "post", mock_post)
    response = requests.post(f"{BASE_URL}/orders", json=payload)
    assert response.status_code == 401
    
   
def test_valid_order_with_multiple_products():
    payload = {
        "status": "pending",
        "products": [
            {"product_id": 1, "quantity": 2},
            {"product_id": 2, "quantity": 3}
        ]
    }
    response = requests.post(f"{BASE_URL}/orders", json=payload)
    assert response.status_code == 200
    