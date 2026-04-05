import pytest
import json
from app import app  # Import the Flask app
from unittest.mock import patch

# Create a test client using Flask's built-in testing features
@pytest.fixture
def client():
    app.testing = True  # Enable testing mode
    with app.test_client() as client:
        yield client

# ------------------------------
# Test GET all items
# ------------------------------
def test_get_inventory(client):
    response = client.get("/inventory")
    assert response.status_code == 200
    data = response.get_json()
    # Ensure the inventory returns a list and has at least the initial items
    assert isinstance(data, list)
    assert len(data) >= 2
    # Check for specific keys in the first item
    for key in ["id", "product_name", "brand", "price", "stock"]:
        assert key in data[0]

# ------------------------------
# Test GET single item by ID
# ------------------------------
def test_get_single_item(client):
    response = client.get("/inventory/1")
    assert response.status_code == 200
    item = response.get_json()
    # Confirm the returned item has expected keys
    for key in ["id", "product_name", "brand", "price", "stock"]:
        assert key in item
    assert item["id"] == 1

# ------------------------------
# Test GET non-existent item returns 404
# ------------------------------
def test_get_item_not_found(client):
    response = client.get("/inventory/999")
    assert response.status_code == 404
    data = response.get_json()
    assert data["error"] == "item not found"

# ------------------------------
# Test POST / add new item
# ------------------------------
def test_add_item(client):
    new_item = {
        "product_name": "Test Milk",
        "brand": "TestBrand",
        "price": 2.5,
        "stock": 10
    }
    response = client.post("/inventory", json=new_item)
    assert response.status_code == 201
    data = response.get_json()
    # Confirm all fields match the request
    for key in new_item:
        assert data[key] == new_item[key]
    # ID should be automatically assigned
    assert "id" in data

# ------------------------------
# Test PATCH / update item
# ------------------------------
def test_update_item(client):
    # Update price and stock for item 1
    update_data = {
        "price": 9.99,
        "stock": 50
    }
    response = client.patch("/inventory/1", json=update_data)
    assert response.status_code == 200
    item = response.get_json()
    # Confirm updated fields changed
    assert item["price"] == 9.99
    assert item["stock"] == 50
    # Confirm other fields remain unchanged
    assert item["product_name"] == "Organic Almond Milk"
    assert item["brand"] == "Silk"

# ------------------------------
# Test PATCH / update non-existent item
# ------------------------------
def test_update_item_not_found(client):
    response = client.patch("/inventory/999", json={"price": 1})
    assert response.status_code == 404

# ------------------------------
# Test DELETE / remove item
# ------------------------------
def test_delete_item(client):
    # First add a temporary item to delete
    temp_item = {"product_name": "DeleteMe", "brand": "TempBrand", "price": 1.1, "stock": 1}
    post_response = client.post("/inventory", json=temp_item)
    item_id = post_response.get_json()["id"]

    # Now delete it
    delete_response = client.delete(f"/inventory/{item_id}")
    assert delete_response.status_code == 200
    deleted_item = delete_response.get_json()["item"]
    # Confirm deleted item matches what we added
    assert deleted_item["id"] == item_id
    assert deleted_item["product_name"] == "DeleteMe"

# ------------------------------
# Test DELETE / non-existent item returns 404
# ------------------------------
def test_delete_item_not_found(client):
    response = client.delete("/inventory/999")
    assert response.status_code == 404


# Test fetch_product function with mocked API response

@patch("cli.requests.get")  # Mock requests.get in the CLI module
def test_fetch_product_mock(mock_get):
    # Mock a successful OpenFoodFacts API response
    mock_response = {
        "status": 1,
        "product": {
            "product_name": "Mocked Chocolate",
            "brands": "MockBrand",
            "ingredients_text": "Sugar, Cocoa, Milk"
        }
    }
    mock_get.return_value.status_code = 200
    mock_get.return_value.json.return_value = mock_response

    # Normally fetch_product() interacts with input(), so we patch it
    from cli import fetch_product
    with patch("builtins.input", side_effect=["mockbarcode", "y", "3.5", "10"]):
        with patch("cli.print_item") as mock_print:
            fetch_product()
            # Check that print_item was called (meaning product added successfully)
            assert mock_print.called