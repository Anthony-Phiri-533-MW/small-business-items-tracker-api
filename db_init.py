from app import app, db  # Import your Flask app and db instance

# Create an application context
with app.app_context():
    # Perform your database operations within the context
    db.create_all()
