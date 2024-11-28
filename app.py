from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_mail import Mail
import os

# Initialize extensions (not tied to an app yet)
db = SQLAlchemy()
migrate = Migrate()
mail = Mail()

def create_app():
    app = Flask(__name__)
    app.config.from_object('config.Config')  # Load configuration from config.py

    # Initialize extensions with the app
    db.init_app(app)
    migrate.init_app(app, db)
    mail.init_app(app)

    # Import routes explicitly and register them
    from routes import setup_routes
    setup_routes(app)  # Pass the app to a function in routes.py to attach routes

    return app


if __name__ == '__main__':
    app = create_app()
    app.run(debug=True)
