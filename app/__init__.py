
# Import necessary modules.
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate

# Import configuration settings from config.py.
from config import Config

# Initialize SQLAlchemy and migration engine.
db = SQLAlchemy()
migrate = Migrate()

# Define a function to create the Flask application.
def create_app(config_class=Config):
    # Initialize Flask application.
    flask_app = Flask(__name__, template_folder='templates', static_folder='static')
    # Load configuration settings from the Config class.
    flask_app.config.from_object(config_class)  

    # Initialize SQLAlchemy with the Flask application.
    db.init_app(flask_app)
    # Initialize migration engine with the Flask application and SQLAlchemy instance.
    migrate.init_app(flask_app, db)

    return flask_app

# Import modules at the bottom to avoid circular imports.
from app import models