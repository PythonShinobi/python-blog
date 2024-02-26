
# Import necessary modules.
import jwt
from time import time
from flask import current_app
from flask_login import UserMixin
from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy import Integer, String
from werkzeug.security import generate_password_hash

# Import the SQLAlchemy instance from the app module.
from app import db, login_manager

# Define the User model class.
class User(UserMixin, db.Model):
    __tablename__ = 'users'
    # Define columns with their types and properties.
    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    name: Mapped[str] = mapped_column(String(100))
    email: Mapped[str] = mapped_column(String(100), unique=True)
    password: Mapped[str] = mapped_column(String(100))

    # Define a representation method for easier debugging.
    def __repr__(self):
        return f'<User {self.username}>'  # Return a string representation of the User object.
    
    def set_password(self, password):
        self.password = generate_password_hash(
            password,
            method='pbkdf2:sha256',
            salt_length=8,
        )
    
    def get_reset_password_token(self, expires_in=600):
        """Return a JWT token as a string, which is generated directly by the jwt.encode() function."""
        return jwt.encode({'reset_password': self.id, 'exp': time() + expires_in}, current_app.config['SECRET_KEY'], algorithm='HS256')
    
    @staticmethod
    def verify_reset_password_token(token):
        """Return the id of a user after decoding the token."""
        try:
            id = jwt.decode(token, current_app.config['SECRET_KEY'], algorithms=['HS256'])['reset_password']
        except:
            return
        # Return a user with the obtained id from the User model.
        return db.session.get(User, id)
    
@login_manager.user_loader
def load_user(user_id):
    return db.get_or_404(User, user_id)