# Small Business Items Tracker API

A Flask API to track items for a small business.

---

## 📖 API Documentation

This is a simple RESTful API for managing records in a store.  
It allows you to perform **CRUD (Create, Read, Update, Delete)** operations on store records.  

- **Framework**: Python (Flask)  
- **Database**: SQLAlchemy  
- **Serialization**: Marshmallow  

---

## ⚙️ Installation

Before using this API, set up the required dependencies and environment.

### Prerequisites
- Python **3.6+**
- Flask
- Flask-SQLAlchemy
- Flask-Marshmallow
- Flask-CORS

### Installation Steps

1. Clone this repository:

   ```bash
   git clone https://github.com/your-username/small-business-items-tracker-api.git
   cd small-business-items-tracker-api
   ```
2. Install dependencies:
   ```batch
   pip install Flask Flask-SQLAlchemy Flask-Marshmallow Flask-CORS
   ```
3. Run the API:
   ```
    python api.py

  The API will now be available at:

        http://127.0.0.1:5000/
    

4.Endpoints
➕ Add a Record
URL: /records

Method: POST

Request Body:

amount (integer): Amount of the item

item (string): Name of the item

record_date (string): Date when the record was created

Example Request:

```json
{
  "amount": 10,
  "item": "Widget",
  "record_date": "2023-11-03"
}
```
📋 Get All Records

URL: /records

Method: GET

Response:
Array of records in JSON format

🔍 Get a Single Record
URL: /records/<int:id>

Method: GET

Parameters:

id (integer): Unique identifier of the record

Response:
Record details in JSON format

✏️ Update a Record
URL: /records/<int:id>

Method: PUT

Parameters:

id (integer): Unique identifier of the record

Request Body:

amount (integer): Updated amount

item (string): Updated item name

record_date (string): Updated record date

Example Request:

```json

{
  "amount": 15,
  "item": "New Widget",
  "record_date": "2023-11-04"
}
```

❌ Delete a Record
URL: /records/<int:id>

Method: DELETE

Parameters:

id (integer): Unique identifier of the record

Response:
Deleted record details in JSON format

🗂 Data Schema
Each record follows this schema:

id (integer): Unique identifier

amount (integer): Amount of the item

item (string): Name of the item

record_date (string): Date when the record was created

🛠 Usage
You can use this API to create, retrieve, update, and delete store records.

Interact using command-line tools like cURL

Or build a frontend application to consume the API

💡 Feel free to modify and extend this API to suit your business needs.
