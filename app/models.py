
# Import necessary modules.
import jwt
from time import time
from flask import current_app
from flask_login import UserMixin
from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy import Integer, String, Text
from werkzeug.security import generate_password_hash
from sqlalchemy.orm import relationship

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
    # The "author" refers to the author property in the BlogPost class.
    # This will act like a list of BlogPost objects attached to each User.
    posts = relationship('BlogPost', back_populates='author')
    # Parent relationship: "comment_author" refers to the comment_author property in the Comment class.    
    comments = relationship("Comment", back_populates="comment_author", cascade="all, delete-orphan")

    # Define a representation method for easier debugging.
    def __repr__(self):
        return f'{self.name}'  # Return a string representation of the User object.
    
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
    
class BlogPost(db.Model):
    __tablename__ = 'blog_posts'
    # Define columns with their types and properties.
    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    # Create Foreign Key, "users.id" the users refers to the tablename of User.
    author_id: Mapped[int] = mapped_column(Integer,  db.ForeignKey("users.id"))
    # Create reference to the User object. The "posts" refers to the posts property in the User class.
    author = relationship('User', back_populates='posts')
    title: Mapped[str] = mapped_column(String(250), unique=True, nullable=False)
    subtitle: Mapped[str] = mapped_column(String(250), nullable=False)
    date: Mapped[str] = mapped_column(String(250), nullable=False)
    body: Mapped[str] = mapped_column(Text, nullable=False)
    img_url: Mapped[str] = mapped_column(String(250), nullable=False)
    # Parent relationship to the comments
    comments = relationship("Comment", back_populates="parent_post")    

    def __repr__(self) -> str:
        return f'{self.author}'
    
# Create a table for the comments on the blog posts
class Comment(db.Model):
    __tablename__ = 'comments'
    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    text: Mapped[str] = mapped_column(Text, nullable=False)
    # Child relationship:"users.id" The users refers to the tablename of the User class.
    # "comments" refers to the comments property in the User class.
    author_id: Mapped[int] = mapped_column(Integer, db.ForeignKey("users.id"))
    comment_author = relationship("User", back_populates="comments")
    # Child Relationship to the BlogPosts
    post_id: Mapped[str] = mapped_column(Integer, db.ForeignKey("blog_posts.id"))
    parent_post = relationship("BlogPost", back_populates="comments")

@login_manager.user_loader
def load_user(user_id):
    return db.get_or_404(User, user_id)