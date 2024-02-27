
# Import necessary modules.
import os
import logging
from logging.handlers import SMTPHandler, RotatingFileHandler
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_login import LoginManager
from flask_bootstrap import Bootstrap5
from flask_mail import Mail
from flask_ckeditor import CKEditor
from flask_gravatar import Gravatar

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
ckeditor = CKEditor()

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
    # Initialize flask_ckeditor with the Flask application.
    ckeditor.init_app(flask_app)
    # Initialize Gravatar object with credentials
    Gravatar(
        flask_app,
        size=100,
        rating='g',
        default='retro',
        force_default=False,
        force_lower=False,
        use_ssl=False,
        base_url=None
    )

    # Register the authentication blueprint.
    from app.auth import bp as auth_bp
    flask_app.register_blueprint(auth_bp)
    # Register the main blueprint.
    from app.main import bp as main_bp
    flask_app.register_blueprint(main_bp)

    if not flask_app.debug and not flask_app.testing:
        if flask_app.config['MAIL_SERVER']:
            auth = None
            if flask_app.config['MAIL_USERNAME'] or flask_app.config['MAIL_PASSWORD']:
                auth = (flask_app.config['MAIL_USERNAME'], flask_app.config['MAIL_PASSWORD'])
            secure = None
            if flask_app.config['MAIL_USE_TLS']:
                secure = ()
            mailHandler = SMTPHandler(
                mailhost=(flask_app.config['MAIL_SERVER'], flask_app.config['MAIL_PORT']),
                fromaddr=f'no-reply@{flask_app.config["MAIL_SERVER"]}',
                toaddrs=flask_app.config['ADMIN'], subject='Flask Application Failure',
                credentials=auth,
                secure=secure,
            )
            mailHandler.setLevel(logging.ERROR)
            flask_app.logger.addHandler(mailHandler)

        # Check if the 'logs' directory exists; if not, create it.
        if not os.path.exists('logs'):
            os.mkdir('logs')

        # Set up a rotating file handler to manage log files.
        fileHandler = RotatingFileHandler(
            'logs/python-blog.log',   # Log file path
            maxBytes=10240,      # Maximum size of each log file (in bytes)
            backupCount=10       # Number of backup log files to keep
        )

        # Set the log message format.
        fileHandler.setFormatter(
            logging.Formatter(
                # the timestamp, log level, message, and the file path and line number where the log message originated.
                '%(asctime)s %(levelname)s: %(message)s [in %(pathname)s:%(lineno)d]'
            )
        )

        # Set the logging level for the file handler to INFO.
        fileHandler.setLevel(logging.INFO)

        # Add the file handler to the Flask application logger.
        flask_app.logger.addHandler(fileHandler)

        # Set the logging level for the Flask application logger to INFO.
        flask_app.logger.setLevel(logging.INFO)

        # Log a message indicating the startup of the Meetup application.
        flask_app.logger.info('Python blog')

    return flask_app

# Import modules at the bottom to avoid circular imports.
from app import models