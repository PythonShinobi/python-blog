
"This file contains configuration settings for the application."

import os
from dotenv import load_dotenv

basedir = os.path.abspath(os.path.dirname(__file__))

ENV = '.env'
load_dotenv(ENV)  # Load the variables in the .env file.

class Config:
    SECRET_KEY = os.getenv('SECRET_KEY') or 'you-will-never-guess'
    SQLALCHEMY_DATABASE_URI = os.getenv('DATABASE_URL') or \
        f'sqlite:///{os.path.join(basedir, "app.db")}'
    MAIL_SERVER = os.getenv('MAIL_SERVER')
    MAIL_PORT = int(os.getenv('MAIL_PORT') or 25)
    MAIL_USE_TLS = os.getenv('MAIL_USE_TLS') is not None
    ADMIN_EMAIL = os.getenv('ADMIN_EMAIL')
    ADMIN_EMAIL_PASSWORD = os.getenv('ADMIN_EMAIL_PASSWORD')
    EMAIL_NOTIFICATION_ERROR = os.getenv('ERROR_NOTIFICATION_EMAIL')
    EMAIL_NOTIFICATION_ERROR_PASSWORD = os.getenv('ERROR_NOTIFICATION_EMAIL_PASSWORD')
