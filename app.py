from flask import Flask, jsonify, request

# create the Flask app
app = Flask(__name__)

# this is just a temporary "database"
# we're using a list of dictionaries instead of a real DB for now
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
    }
]

# basic route to check if server is running
@app.route("/")
def home():
    return "Inventory API is running "


# GET all inventory items
# just returns the whole list as JSON
@app.route("/inventory", methods=["GET"])
def get_inventory():
    return jsonify(inventory)


# GET a single item by its id
@app.route("/inventory/<int:item_id>", methods=["GET"])
def get_item(item_id):
    # loop through inventory to find the matching item
    for item in inventory:
        if item["id"] == item_id:
            return jsonify(item)

    # if item not found, return an error message
    return jsonify({"error": "item not found"}), 404   


# POST - add a new item to the inventory
@app.route("/inventory", methods=["POST"])
def add_item():
    # get JSON data sent from the client (converted to Python dict)
    data = request.get_json()

    # create a new item using the data received
    new_item = {
        # simple way to generate an id (not perfect, but fine for now)
        "id": len(inventory) + 1,
        "product_name": data.get("product_name"),
        "brand": data.get("brand"),
        "price": data.get("price"),
        "stock": data.get("stock")
    }

    # add the new item to our "database"
    inventory.append(new_item)

    # return the created item with 201 status (created)
    return jsonify(new_item), 201 

# PATCH - update an existing item (partial update)
@app.route("/inventory/<int:item_id>", methods=["PATCH"])
def update_item(item_id):
    # get incoming data from client
    data = request.get_json()

    # find the item we want to update
    for item in inventory:
        if item["id"] == item_id:

            # update only fields that were sent
            if "product_name" in data:
                item["product_name"] = data["product_name"]

            if "brand" in data:
                item["brand"] = data["brand"]

            if "price" in data:
                item["price"] = data["price"]

            if "stock" in data:
                item["stock"] = data["stock"]

            # return updated item
            return jsonify(item)

    # if item not found
    return jsonify({"error": "item not found"}), 404

# DELETE - remove an item from inventory
@app.route("/inventory/<int:item_id>", methods=["DELETE"])
def delete_item(item_id):
    # loop using index so we can safely remove item
    for i in range(len(inventory)):
        if inventory[i]["id"] == item_id:
            deleted_item = inventory.pop(i)  # remove item

            # return what was deleted (useful for confirmation)
            return jsonify({
                "message": "item deleted",
                "item": deleted_item
            })

    # if item not found
    return jsonify({"error": "item not found"}), 404


# run the app
if __name__ == "__main__":
    app.run(debug=True)