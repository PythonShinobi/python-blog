
# Import necessary modules.
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_login import LoginManager
from flask_bootstrap import Bootstrap5
from flask_mail import Mail
from flask_wtf.csrf import CSRFProtect

# Import configuration settings from config.py.
from config import Config

# Initialize SQLAlchemy and migration engine.
db = SQLAlchemy()
migrate = Migrate()
login_manager = LoginManager()  # Initialize login manager.
# Specify the view function that Flask-Login should redirect users to when they need to log in.
login_manager.login_view = 'auth.login'
bootstrap = Bootstrap5()
mail = Mail()
csrf = CSRFProtect()

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
    # Initialize login manager with the Flask application.
    login_manager.init_app(flask_app)
    # Initialize bootstrap with the Flask application.
    bootstrap.init_app(flask_app)
    # Initialize flask_mail with the Flask application.
    mail.init_app(flask_app)
    # Initialize csrf protection with the Flask application.
    csrf.init_app(flask_app)

    # Register the authentication blueprint.
    from app.auth import bp as auth_bp
    flask_app.register_blueprint(auth_bp)
    # Register the main blueprint.
    from app.main import bp as main_bp
    flask_app.register_blueprint(main_bp)

    return flask_app

# Import modules at the bottom to avoid circular imports.
from app import models