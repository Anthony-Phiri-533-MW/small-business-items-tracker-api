from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_marshmallow import Marshmallow
import os
from datetime import datetime, timezone
from flask_cors import CORS
from flask_migrate import Migrate
from flask_bcrypt import Bcrypt
from flask_restx import Api, Resource, fields

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

# Flask migrate
migrate = Migrate(app, db)

# Initialize Flask-Bcrypt
bcrypt = Bcrypt(app)

# Initialize Flask-RESTX API
api = Api(app, doc="/docs")  # Swagger UI will be available at /docs

# Product class/model
class StoreData(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    amount = db.Column(db.Integer)
    item = db.Column(db.String(240))
    record_date = db.Column(db.DateTime, default=lambda: datetime.now(timezone.utc))

    def __init__(self, amount, item):
        self.amount = amount
        self.item = item

# User data class
class StoreUserRecords(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(240), unique=True, nullable=False)
    password = db.Column(db.String(240), nullable=False)

    def __init__(self, name, password):
        self.name = name
        self.password = bcrypt.generate_password_hash(password).decode('utf-8')

    def check_password(self, password):
        return bcrypt.check_password_hash(self.password, password)

# Expense Schema
class DataSchema(ma.Schema):
    class Meta:
        fields = ('id', 'amount', 'item', 'record_date')

# User Schema
class UserSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = StoreUserRecords
        fields = ('id', 'name', 'password')

# Initialize schemas
data_schema = DataSchema()
data_schemas = DataSchema(many=True)
user_schema = UserSchema()
users_schema = UserSchema(many=True)

# Define Swagger models using Flask-RESTX
store_data_model = api.model('StoreData', {
    'amount': fields.Integer(required=True, description='Amount of the item'),
    'item': fields.String(required=True, description='Name of the item'),
    'record_date': fields.String(required=False, description='Record date (Optional)', default=datetime.utcnow().isoformat())
})

user_model = api.model('StoreUserRecords', {
    'name': fields.String(required=True, description='Username'),
    'password': fields.String(required=True, description='Password')
})

# Create a route to add a record
@api.route('/records')
class RecordList(Resource):
    @api.doc(description="Create a new store record")
    @api.expect(store_data_model, validate=True)
    def post(self):
        data = request.json
        new_record = StoreData(amount=data['amount'], item=data['item'])
        db.session.add(new_record)
        db.session.commit()
        return data_schema.jsonify(new_record), 201

    @api.doc(description="Get all store records")
    def get(self):
        all_records = StoreData.query.all()
        return data_schemas.dump(all_records), 200

# Create a route to get a single record
@api.route('/records/<int:id>')
class Record(Resource):
    @api.doc(description="Get a store record by ID")
    def get(self, id):
        record = StoreData.query.get(id)
        if record:
            return data_schema.jsonify(record)
        return {'message': 'Record not found'}, 404

# Create a route to update a record
@api.route('/records/<int:id>')
class RecordUpdate(Resource):
    @api.doc(description="Update a store record by ID")
    @api.expect(store_data_model, validate=True)
    def put(self, id):
        record = StoreData.query.get(id)
        if record:
            data = request.json
            record.amount = data['amount']
            record.item = data['item']
            record.record_date = data.get('record_date', record.record_date)
            db.session.commit()
            return data_schema.jsonify(record)
        return {'message': 'Record not found'}, 404

# Delete a record
@api.route('/records/<int:id>')
class RecordDelete(Resource):
    @api.doc(description="Delete a store record by ID")
    def delete(self, id):
        record = StoreData.query.get(id)
        if record:
            db.session.delete(record)
            db.session.commit()
            return data_schema.jsonify(record)
        return {'message': 'Record not found'}, 404

# Routes for managing users
@api.route('/users')
class UserList(Resource):
    @api.doc(description="Create a new user")
    @api.expect(user_model, validate=True)
    def post(self):
        data = request.json
        new_user = StoreUserRecords(name=data['name'], password=data['password'])
        db.session.add(new_user)
        db.session.commit()
        return user_schema.jsonify(new_user), 201

    @api.doc(description="Get all users")
    def get(self):
        all_users = StoreUserRecords.query.all()
        return users_schema.dump(all_users), 200

# Route to get a single user by ID
@api.route('/users/<int:id>')
class User(Resource):
    @api.doc(description="Get a user by ID")
    def get(self, id):
        user = StoreUserRecords.query.get_or_404(id)
        return user_schema.jsonify(user)

# Route to update a user
@api.route('/users/<int:id>')
class UserUpdate(Resource):
    @api.doc(description="Update a user by ID")
    @api.expect(user_model, validate=True)
    def put(self, id):
        user = StoreUserRecords.query.get_or_404(id)
        data = request.json
        user.name = data['name']
        user.password = data['password']
        db.session.commit()
        return user_schema.jsonify(user)

# Route to delete a user
@api.route('/users/<int:id>')
class UserDelete(Resource):
    @api.doc(description="Delete a user by ID")
    def delete(self, id):
        user = StoreUserRecords.query.get_or_404(id)
        db.session.delete(user)
        db.session.commit()
        return user_schema.jsonify(user)

# Authentication routes
@api.route('/register')
class Register(Resource):
    @api.doc(description="Register a new user")
    @api.expect(user_model, validate=True)
    def post(self):
        data = request.json
        existing_user = StoreUserRecords.query.filter_by(name=data['name']).first()
        if existing_user:
            return {'message': 'User already exists'}, 400
        new_user = StoreUserRecords(name=data['name'], password=data['password'])
        db.session.add(new_user)
        db.session.commit()
        return user_schema.jsonify(new_user), 201

@api.route('/login')
class Login(Resource):
    @api.doc(description="Login a user")
    @api.expect(user_model, validate=True)
    def post(self):
        data = request.json
        user = StoreUserRecords.query.filter_by(name=data['name']).first()
        if user and user.check_password(data['password']):
            return {'message': 'Login successful', 'user': user_schema.dump(user)}, 200
        return {'message': 'Invalid credentials'}, 401

# Run the server
if __name__ == '__main__':
    app.run(host=os.getenv('HOST', '0.0.0.0'), port=int(os.getenv('PORT', 8080)), debug=False)

