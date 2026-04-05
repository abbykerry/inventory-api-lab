import pytest
from app import app

@pytest.fixture
def client():
    app.config["TESTING"] = True
    return app.test_client()

def test_get_all_items(client):
    response = client.get("/inventory")
    assert response.status_code == 200

def test_create_item(client):
    new_item = {
        "product_name": "Test Product",
        "brand": "Test Brand",
        "price": 1.99,
        "stock": 10
    }

    response = client.post("/inventory", json=new_item)
    assert response.status_code == 201
    data = response.get_json()
    assert data["product_name"] == "Test Product"

def test_get_single_item(client):
    # Create item first
    new_item = {
        "product_name": "Single Test",
        "brand": "BrandX",
        "price": 2.50,
        "stock": 5
    }

    res = client.post("/inventory", json=new_item)
    item_id = res.get_json()["id"]

    # fetch 
    response = client.get(f"/inventory/{item_id}")
    assert response.status_code == 200

    data = response.get_json()
    assert data["product_name"] == "Single Test"

def test_delete_item(client):
    # Create item first
    new_item = {
        "product_name": "Delete Test",
        "brand": "BrandY",
        "price": 3.00,
        "stock": 8
    }

    res = client.post("/inventory", json=new_item)
    item_id = res.get_json()["id"]

    # Delete it
    response = client.delete(f"/inventory/{item_id}")
    assert response.status_code == 200

    # Confirm it's gone
    response = client.get(f"/inventory/{item_id}")
    assert response.status_code == 404