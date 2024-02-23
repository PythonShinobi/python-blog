
from flask import render_template, redirect, url_for, request, session
from flask_login import current_user

from app.main import bp

@bp.route('/', methods=['GET', 'POST'])
def get_all_posts():
    return render_template('index.html')

@bp.route('/about')
def about():
    # Check if the user is authenticated.
    if not current_user.is_authenticated:
        # Store the requested URL in the session.
        session['next'] = request.path
        # Redirect to the login page.
        return redirect(url_for('auth.login'))
    # If the user is authenticated, render the about page.
    return render_template('about.html')

@bp.route('/contact')
def contact():
    # Check if the user is authenticated.
    if not current_user.is_authenticated:
        # Store the requested URL in the session.
        session['next'] = request.path
        # Redirect to the login page.
        return redirect(url_for('auth.login'))
    # If the user is authenticated, render the contact page.
    return render_template('contact.html')