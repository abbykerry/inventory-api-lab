# Inventory API Project

## Description
This project is an Inventory Management API built using **Flask**.  
It allows users to **create, read, update, and delete** inventory items and includes a **CLI interface** for easy interaction.  
Additionally, products can be fetched from the **OpenFoodFacts API** and added to the local inventory.

---

## Features

- **CRUD operations** via Flask routes:
  - `GET /inventory` — list all items
  - `GET /inventory/<id>` — get a single item by ID
  - `POST /inventory` — add a new item
  - `PATCH /inventory/<id>` — update existing item
  - `DELETE /inventory/<id>` — delete an item

- **Command-Line Interface (CLI)**:
  - List, get, add, update, delete inventory items
  - Fetch product information from OpenFoodFacts and optionally add it to inventory

- **Integration with OpenFoodFacts API**:
  - Search by barcode or product name
  - Display product details (name, brand, ingredients)
  - Optionally add fetched products to local inventory

- **Unit testing** with `pytest` covering all routes and features

---

## Getting Started

### Prerequisites
- Python 3.10 or higher
- `pip` or `pipenv` to install dependencies
- Internet connection (for fetching products from OpenFoodFacts)

### Installation

1. **Clone the repository**:

```bash
git clone <your-repo-link>

Navigate into the project directory:

cd inventory-api-lab

Create and activate a virtual environment (recommended):

python3 -m venv venv
source venv/bin/activate  # macOS/Linux
venv\Scripts\activate     # Windows

Install dependencies:

pip install -r requirements.txt
# OR if using pipenv:
pipenv install

Running the Application
1. Start the Flask API
python app.py

The API will run at: http://127.0.0.1:5000/

2. Run the CLI

In a separate terminal:

python cli.py

Follow the interactive menu to list, add, update, delete, or fetch products.

Testing

Run the unit tests using pytest:

pytest

All routes and features are covered, including CRUD and OpenFoodFacts integration.

Inventory

The project includes a mock database (Python list) to store items.
Sample items included:

ID	Product Name	Brand	Price	Stock
1	Organic Almond Milk	Silk	5.99	10
2	Whole Wheat Bread	Nature's Own	3.49	20