from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_marshmallow import Marshmallow
import os
from datetime import datetime
from flask_cors import CORS
from flask_migrate import Migrate

# Initialize the Flask app
app = Flask(__name__)
CORS(app)
basedir = os.path.abspath(os.path.dirname(__file__))

# Configure the database
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + os.path.join(basedir, 'db.sqlite')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# Initialize the SQLAlchemy database
db = SQLAlchemy(app)

# Initialize Marshmallow
ma = Marshmallow(app)

#flask migrate
migrate = Migrate(app, db)

# Product class/model
class StoreData(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    amount = db.Column(db.Integer)
    item = db.Column(db.String(240))
    #record_date = db.Column(db.DateTime, default=datetime.utcnow)
    record_date = db.Column(db.String(240))

    def __init__(self, amount, item, record_date):
        self.amount = amount
        self.item = item
        self.record_date = record_date

#User data class
class StoreUserRecords(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(240), unique=True, nullable=False)
    password = db.Column(db.String(240), nullable=False)

    def __init__(self, name, password):
        self.name = name
        self.password = password

# Expense Schema
class DataSchema(ma.Schema):
    class Meta:
        fields = ('id', 'amount', 'item', 'record_date')  # Corrected 'record_data' to 'record_date'

# User Schema
class UserSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = StoreUserRecords
        fields = ('id', 'name', 'password')  # Define fields to serialize

# Initialize the schema
data_schema = DataSchema()
data_schemas = DataSchema(many=True)  # Corrected 'data_Shemas' to 'data_schemas'

# Initialize the user schema
user_schema = UserSchema()
users_schema = UserSchema(many=True)

# Create a route to add a record
@app.route('/records', methods=['POST'])
def add_record():
    amount = request.json['amount']
    item = request.json['item']
    record_date = request.json['record_date']

    new_record = StoreData(amount=amount, item=item, record_date=record_date)

    db.session.add(new_record)
    db.session.commit()

    return data_schema.jsonify(new_record)

# Create a route to get records
@app.route('/records', methods=['GET'])
def get_records():
    all_records = StoreData.query.all()
    results = data_schemas.dump(all_records)  # Corrected 'data_schema' to 'data_schemas'

    return jsonify(results)

# Create a route to get a single record
@app.route('/records/<int:id>', methods=['GET'])
def get_record(id):
    record = StoreData.query.get(id)
    return data_schema.jsonify(record)

# Create a route to update a record
@app.route('/records/<int:id>', methods=['PUT'])
def update_record(id):
    record = StoreData.query.get(id)

    amount = request.json['amount']
    item = request.json['item']
    record_date = request.json['record_date']

    record.amount = amount
    record.item = item
    record.record_date = record_date 

    db.session.commit()

    return data_schema.jsonify(record)

    #return data_schema.jsonify(new_record)

#Delete a record
@app.route('/records/<int:id>', methods=['DELETE'])
def delete_record(id):
    record = StoreData.query.get(id)
    db.session.delete(record)

    db.session.commit()
    
    return data_schema.jsonify(record)


#Routes for managing users
# Route to create a new user
@app.route('/users', methods=['POST'])
def add_user():
    name = request.json['name']
    password = request.json['password']

    new_user = StoreUserRecords(name=name, password=password)

    db.session.add(new_user)
    db.session.commit()

    return user_schema.jsonify(new_user)

# Route to get all users
@app.route('/users', methods=['GET'])
def get_users():
    all_users = StoreUserRecords.query.all()
    result = users_schema.dump(all_users)
    return jsonify(result)

# Route to get a single user by ID
@app.route('/users/<int:id>', methods=['GET'])
def get_user(id):
    user = StoreUserRecords.query.get_or_404(id)
    return user_schema.jsonify(user)

# Route to update a user by ID
@app.route('/users/<int:id>', methods=['PUT'])
def update_user(id):
    user = StoreUserRecords.query.get_or_404(id)

    name = request.json['name']
    password = request.json['password']

    user.name = name
    user.password = password

    db.session.commit()

    return user_schema.jsonify(user)

# Route to delete a user by ID
@app.route('/users/<int:id>', methods=['DELETE'])
def delete_user(id):
    user = StoreUserRecords.query.get_or_404(id)

    db.session.delete(user)
    db.session.commit()

    return user_schema.jsonify(user)

# Run the server
if __name__ == '__main__':
    app.run(debug=True, port=5001)
