from flask import Flask, jsonify, request

app = Flask(__name__)

# This list acts as our temporary "database". Each item is a dictionary representing a product.
# It's in-memory, so every time the server restarts, we lose added/edited items.
# mock database (array)
inventory = [
    {
        "id": 1,
        "product_name": "Organic Almond Milk",
        "brand": "Silk",
        "price": 5.99,
        "stock": 10
    },
    {
        "id": 2,
        "product_name": "Whole Wheat Bread",
        "brand": "Nature's Own",
        "price": 3.49,
        "stock": 20
    },
    {
        "id": 3,
        "product_name": "Greek Yogurt",
        "brand": "Chobani",
        "price": 1.99,
        "stock": 15
    },
    {
        "id": 4,
        "product_name": "Apple Juice",
        "brand": "Tropicana",
        "price": 2.49,
        "stock": 12
    }
]

# Basic route to make sure the server is running. Useful for quick checks before hitting API endpoints.
@app.route("/")
def home():
    return "Inventory API is running"

# Return the entire inventory list. This is how a client can see everything currently stored.
@app.route("/inventory", methods=["GET"])
def get_inventory():
    return jsonify(inventory)

# Fetch a single item by its ID. If it's not found, return a 404 error.
@app.route("/inventory/<int:item_id>", methods=["GET"])
def get_item(item_id):
    for item in inventory:
        if item["id"] == item_id:
            return jsonify(item)
    # We return a 404 error if the item doesn't exist so the client knows their request failed.
    return jsonify({"error": "item not found"}), 404

# Add a new item to the inventory. Includes validation to make sure the input is correct.
@app.route("/inventory", methods=["POST"])
def add_item():
    data = request.get_json()  # Convert incoming JSON payload to a Python dictionary

    # Reject empty requests immediately
    if not data:
        return jsonify({"error": "no data provided"}), 400

    # Define which fields are mandatory
    required_fields = ["product_name", "brand", "price", "stock"]

    # Make sure all required fields exist, otherwise give the user an error explaining which one is missing
    for field in required_fields:
        if field not in data:
            return jsonify({"error": f"{field} is required"}), 400

    # Validate that price is a number and stock is an integer
    if not isinstance(data["price"], (int, float)):
        return jsonify({"error": "price must be a number"}), 400
    if not isinstance(data["stock"], int):
        return jsonify({"error": "stock must be an integer"}), 400

    # Generate a new ID based on the current length of the list.
    # Note: In a real database, the ID would be handled automatically.
    new_item = {
        "id": len(inventory) + 1,
        "product_name": data["product_name"],
        "brand": data["brand"],
        "price": data["price"],
        "stock": data["stock"]
    }

    inventory.append(new_item)  # Add the validated item to our inventory list

    # Return the newly created item so the client can confirm it was added
    return jsonify(new_item), 201

# Update specific fields of an existing item. Allows partial updates.
@app.route("/inventory/<int:item_id>", methods=["PATCH"])
def update_item(item_id):
    data = request.get_json()
    if not data:
        return jsonify({"error": "no data provided"}), 400

    # Find the item by ID
    for item in inventory:
        if item["id"] == item_id:
            # Only update fields that are included in the request
            if "product_name" in data:
                item["product_name"] = data["product_name"]
            if "brand" in data:
                item["brand"] = data["brand"]
            if "price" in data:
                if not isinstance(data["price"], (int, float)):
                    return jsonify({"error": "price must be a number"}), 400
                item["price"] = data["price"]
            if "stock" in data:
                if not isinstance(data["stock"], int):
                    return jsonify({"error": "stock must be an integer"}), 400
                item["stock"] = data["stock"]

            # Return the updated item so the client can see the new values
            return jsonify(item)

    # If the item doesn't exist, let the client know
    return jsonify({"error": "item not found"}), 404

# Delete an item from the inventory.
@app.route("/inventory/<int:item_id>", methods=["DELETE"])
def delete_item(item_id):
    # Iterate with index so we can safely remove an item while looping
    for index, item in enumerate(inventory):
        if item["id"] == item_id:
            # Pop removes the item from the list and gives us the removed item to return
            removed_item = inventory.pop(index)
            return jsonify({
                "message": "item deleted",
                "item": removed_item
            })
    # If the item wasn't found, return a 404 so the client knows
    return jsonify({"error": "item not found"}), 404

if __name__ == "__main__":
    # Starts the Flask development server. Debug=True will reload automatically on changes.
    app.run(debug=True)