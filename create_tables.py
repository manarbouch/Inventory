from app import app, db

# This ensures that the application context is pushed
with app.app_context():
    # Create all tables in the database based on the models
    db.create_all()

print("All tables created successfully!")
