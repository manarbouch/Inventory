import os

class Config:
    # Set up the base directory
    basedir = os.path.abspath(os.path.dirname(__file__))

    # SQLite database URI configured to be inside the instance folder
    SQLALCHEMY_DATABASE_URI = f'sqlite:///{os.path.join(basedir, "instance", "inventory.db")}'
    SQLALCHEMY_TRACK_MODIFICATIONS = False  # Optional, to avoid warning
    SECRET_KEY = 'your_secret_key'  # Replace with your secret key

    # Flask-Mail configurations (example for Gmail)
    MAIL_USERNAME = os.getenv('MAIL_USERNAME')
    MAIL_PASSWORD = os.getenv('MAIL_PASSWORD')
    MAIL_SERVER = 'smtp.gmail.com'
    MAIL_PORT = 587
    MAIL_USE_TLS = True
