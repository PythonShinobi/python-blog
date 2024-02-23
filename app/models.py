
# Import necessary modules.
from flask_login import UserMixin
from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy import Integer, String

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
    
@login_manager.user_loader
def load_user(user_id):
    return db.get_or_404(User, user_id)