import requests  # to send HTTP requests to our Flask API
import json      # to format JSON output nicely if needed

# Base URL of our Flask API
BASE_URL = "http://127.0.0.1:5000/inventory"

# Helper function to print an item in a readable way
def print_item(item):
    # We're formatting the item nicely so the user can easily see details
    print(f"ID: {item['id']}")
    print(f"Product Name: {item['product_name']}")
    print(f"Brand: {item['brand']}")
    print(f"Price: ${item['price']}")
    print(f"Stock: {item['stock']}")
    print()  # blank line for readability

# Fetch and display all items from the API
def list_items():
    response = requests.get(BASE_URL)
    if response.status_code == 200:
        items = response.json()
        if not items:
            print("Inventory is empty.")
        else:
            for item in items:
                print_item(item)
    else:
        print("Failed to fetch inventory. Try again later.")

# Fetch and display a single item by ID
def get_item(item_id):
    response = requests.get(f"{BASE_URL}/{item_id}")
    if response.status_code == 200:
        print_item(response.json())
    elif response.status_code == 404:
        print(f"No item found with ID {item_id}.")
    else:
        print("Error fetching item.")

# Prompt user for new item details and send a POST request to add it
def add_item():
    print("Enter new product details:")

    # Collect inputs from the user
    product_name = input("Product Name: ").strip()
    brand = input("Brand: ").strip()

    # Make sure the price is a valid number
    while True:
        try:
            price = float(input("Price: ").strip())
            break
        except ValueError:
            print("Price must be a number. Try again.")

    # Make sure the stock is a valid integer
    while True:
        try:
            stock = int(input("Stock: ").strip())
            break
        except ValueError:
            print("Stock must be an integer. Try again.")

    data = {
        "product_name": product_name,
        "brand": brand,
        "price": price,
        "stock": stock
    }

    # Send the POST request to the API to add the item
    response = requests.post(BASE_URL, json=data)
    if response.status_code == 201:
        print("Item added successfully!")
        print_item(response.json())
    else:
        print("Failed to add item.")
        print(response.json())

# Prompt user for ID and fields to update, then send a PATCH request
def update_item():
    try:
        item_id = int(input("Enter ID of the item to update: ").strip())
    except ValueError:
        print("ID must be an integer.")
        return

    print("Leave fields blank to keep current values.")
    product_name = input("New Product Name: ").strip()
    brand = input("New Brand: ").strip()
    price_input = input("New Price: ").strip()
    stock_input = input("New Stock: ").strip()

    data = {}
    if product_name:
        data["product_name"] = product_name
    if brand:
        data["brand"] = brand
    if price_input:
        try:
            data["price"] = float(price_input)
        except ValueError:
            print("Price must be a number.")
            return
    if stock_input:
        try:
            data["stock"] = int(stock_input)
        except ValueError:
            print("Stock must be an integer.")
            return

    if not data:
        print("No updates provided.")
        return

    # Send PATCH request to update the item
    response = requests.patch(f"{BASE_URL}/{item_id}", json=data)
    if response.status_code == 200:
        print("Item updated successfully!")
        print_item(response.json())
    else:
        print("Failed to update item.")
        print(response.json())

# Prompt user for ID and delete the item
def delete_item():
    try:
        item_id = int(input("Enter ID of the item to delete: ").strip())
    except ValueError:
        print("ID must be an integer.")
        return

    # Send DELETE request
    response = requests.delete(f"{BASE_URL}/{item_id}")
    if response.status_code == 200:
        print("Item deleted successfully!")
        print_item(response.json()["item"])
    elif response.status_code == 404:
        print(f"No item found with ID {item_id}.")
    else:
        print("Failed to delete item.")

# Fetch product info from OpenFoodFacts and optionally add to our inventory
def fetch_product():
    print("Search product in OpenFoodFacts")
    query = input("Enter barcode (numbers only): ").strip()

    if not query:
        print("Search cannot be empty.")
        return

    # Using barcode endpoint (more reliable than search endpoint)
    url = f"https://world.openfoodfacts.org/api/v0/product/{query}.json"

    try:
        headers = {
            "User-Agent": "inventory-app/1.0 (learning project)"
            }
        
        response = requests.get(url, headers=headers)

        # If API itself fails (network / server issue)
        if response.status_code != 200:
            print("Error connecting to OpenFoodFacts API.")
            return

        # Convert response to Python dictionary
        data = response.json()

        # status = 1 means product found, 0 means not found
        if data.get("status") != 1:
            print("Product not found.")
            return

        product = data.get("product", {})

        print("\nProduct found:")
        print(f"Name: {product.get('product_name', 'N/A')}")
        print(f"Brand: {product.get('brands', 'N/A')}")
        print(f"Ingredients: {product.get('ingredients_text', 'N/A')}\n")

        # Ask user if they want to add it to inventory
        choice = input("Do you want to add this product to inventory? (y/n): ").strip().lower()

        if choice == "y":
            # We still ask user for price and stock since API doesn't provide reliable values
            new_item = {
                "product_name": product.get("product_name", "Unknown Product"),
                "brand": product.get("brands", "Unknown Brand"),
                "price": float(input("Enter price to assign: ").strip()),
                "stock": int(input("Enter stock quantity: ").strip())
            }

            res = requests.post(BASE_URL, json=new_item)

            if res.status_code == 201:
                print("Product added successfully!")
                print_item(res.json())
            else:
                print("Failed to add product.")
        else:
            print("Product not added.")

    except Exception as e:
        print("Error fetching product:", e)
  

# Main menu loop for the CLI
def menu():
    while True:
        print("\nInventory CLI")
        print("1. List all items")
        print("2. Get item by ID")
        print("3. Add new item")
        print("4. Update existing item")
        print("5. Delete item")
        print("6. Exit")
        print("7. Fetch product from OpenFoodFacts")

        choice = input("Enter choice: ").strip()

        if choice == "1":
            list_items()
        elif choice == "2":
            try:
                item_id = int(input("Enter item ID: ").strip())
                get_item(item_id)
            except ValueError:
                print("ID must be an integer.")
        elif choice == "3":
            add_item()
        elif choice == "4":
            update_item()
        elif choice == "5":
            delete_item()
        elif choice == "7":
            fetch_product()
        elif choice == "6":
            print("Exiting CLI.")
            break
        else:
            print("Invalid choice. Select 1-7.")

if __name__ == "__main__":
    menu()