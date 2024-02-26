
import sqlalchemy

# Import the create_app function from the app module
from app import create_app, db
from app.models import User

# Create the Flask application using the create_app function
flask_app = create_app()

@flask_app.shell_context_processor
def make_shell_context():
    return {'sqlalchemy': sqlalchemy, 'db': db, 'User': User}

# Check if the script is being run directly
if __name__ == '__main__':
    # Run the Flask application on port 5000
    flask_app.run(port=5003)
