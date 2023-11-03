# small-business-items-tracker-api
A flask api to track items for a small business

API Documentation
This is a simple RESTful API for managing records in a store. It allows you to perform CRUD (Create, Read, Update, Delete) operations on store records. The API is built using Python and the Flask framework, and it uses SQLAlchemy for database management and Marshmallow for data serialization.

Installation
Before you can use this API, you need to set up the required dependencies and configure your environment.

Prerequisites
Python 3.6 or higher
Flask
Flask-SQLAlchemy
Flask-Marshmallow
Flask-CORS
Installation Steps
Clone this repository to your local machine.

Install the required dependencies using pip:

bash

pip install Flask Flask-SQLAlchemy Flask-Marshmallow Flask-CORS
Run the API by executing the following command within the project directory:

bash

python api.py
The API should now be running locally at http://127.0.0.1:5000/.

Endpoints
The API provides the following endpoints for managing store records:

Add a Record
URL: /records
Method: POST
Request Body:
amount (integer): The amount of the item.
item (string): The name of the item.
record_date (string): The date when the record was created.
Example Request
json

{
  "amount": 10,
  "item": "Widget",
  "record_date": "2023-11-03"
}
Get All Records
URL: /records
Method: GET
Response:
An array of records in JSON format.
Get a Single Record
URL: /records/<int:id>
Method: GET
Parameters:
id (integer): The unique identifier of the record.
Response:
Details of the record in JSON format.
Update a Record
URL: /records/<int:id>
Method: PUT
Parameters:
id (integer): The unique identifier of the record.
Request Body:
amount (integer): The updated amount of the item.
item (string): The updated name of the item.
record_date (string): The updated date when the record was created.
Example Request
json

{
  "amount": 15,
  "item": "New Widget",
  "record_date": "2023-11-04"
}
Delete a Record
URL: /records/<int:id>
Method: DELETE
Parameters:
id (integer): The unique identifier of the record.
Response:
Details of the deleted record in JSON format.
Data Schema
The data schema used in the API for record representation:

id (integer): Unique identifier of the record.
amount (integer): The amount of the item.
item (string): The name of the item.
record_date (string): The date when the record was created.
Usage
You can use this API to create, retrieve, update, and delete store records. You can interact with the API using various tools, including command-line tools like curl or by building a frontend application that communicates with this API.

Feel free to modify and extend this API to suit your specific requirements. Make sure to handle error cases and implement proper security measures in a production environment.
