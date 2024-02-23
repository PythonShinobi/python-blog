
from flask import render_template, redirect, url_for, flash, request, session
from flask_login import login_user, logout_user, current_user
from werkzeug.security import generate_password_hash, check_password_hash
from urllib.parse import urlsplit, urljoin

from app import db
from app.auth import bp
from app.auth.forms import LoginForm, RegisterForm
from app.models import User

# Define a list of safe endpoints within your application.
SAFE_ENDPOINTS = ['main.about', 'main.contact']

def get_safe_next_page():
    """ Returns the URL of the next page from the 'next' query parameter."""
    next_page = request.args.get('next')  # Retrieve the URL from the 'next' key.
    if next_page:
        # Check if the next_page is a safe endpoint with the application.
        if next_page in SAFE_ENDPOINTS:
            return next_page
        # Check if the next_page is a safe local URL within the application domain.
        if urlsplit(next_page).netloc == '' and urljoin(request.host_url, next_page) == next_page:
            return next_page
        
        return None

# Register new users into the User database.
@bp.route('/register', methods=['GET', 'POST'])
def register():
    # Check if a user is logged in
    if current_user.is_authenticated:
        # Redirect user to the home page if they are logged in.
        return redirect(url_for('main.get_all_posts'))
    
    form = RegisterForm()
    if form.validate_on_submit():
        # Check if user email is already present in the database.
        result = db.session.execute(db.select(User).where(User.email == form.email.data))
        user = result.scalar()
        if user:
            # User already exists
            flash("You've already signed up with that email, log in in")
            return redirect(url_for('auth.login'))
        
        hash_and_salted_password = generate_password_hash(
            form.password.data,
            method='pbkdf2:sha256',
            salt_length=8,
        )
        new_user = User(
            name=form.name.data,
            email=form.email.data,
            password=hash_and_salted_password,
        )
        db.session.add(new_user)
        db.session.commit()
        # This line will authenticate the user with Flask-Login
        login_user(new_user)
        return redirect(url_for('main.get_all_posts'))
    
    return render_template('auth/register.html', form=form, current_user=current_user)

@bp.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('main.get_all_posts'))
    
    form = LoginForm()
    if form.validate_on_submit():
        password = form.password.data
        result = db.session.execute(db.select(User).where(User.email == form.email.data))
        # Note, email in db is unique so will only have one result.
        user = result.scalar()
        # Email doesn't exist
        if not user:
            flash('That email does not exist, please try again.')
            return redirect(url_for('auth.login'))
        # Password is incorrect
        elif not check_password_hash(user.password, password):
            flash('Password incorrect, please try again.')
            return redirect(url_for('auth.login'))
        else:
            login_user(user)
            # Get the next page from the query parameters or session, ensuring its safety.
            next_page = get_safe_next_page()
            if not next_page:
                # Retrieves and removes the value associated with the key 'next' from the session. If there is no such key 
                # in the session, it returns the default value without raising an error.
                next_page = session.pop('next', url_for('main.get_all_posts'))
            # Redirect the user to the safe next page.
            return redirect(next_page)
        
    return render_template('auth/login.html', form=form, current_user=current_user)

@bp.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('main.get_all_posts'))