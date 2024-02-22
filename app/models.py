
# Import necessary modules.
from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy import Integer, String

# Import the SQLAlchemy instance from the app module.
from app import db

# Define the User model class.
class User(db.Model):
    __tablename__ = 'users'
    # Define columns with their types and properties.
    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    name: Mapped[str] = mapped_column(String(100))
    email: Mapped[str] = mapped_column(String(100), unique=True)
    password: Mapped[str] = mapped_column(String(100))

    # Define a representation method for easier debugging.
    def __repr__(self):
        return f'<User {self.username}>'  # Return a string representation of the User object.