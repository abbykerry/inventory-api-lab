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


# run the app
if __name__ == "__main__":
    app.run(debug=True)