
from flask import render_template, redirect, url_for, request, session
from flask_login import current_user

from app.main import bp
from app.main.email import send_email

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

@bp.route('/contact', methods=['GET', 'POST'])
def contact():
    # Check if the user is authenticated.
    if not current_user.is_authenticated:
        # Store the requested URL in the session.
        session['next'] = request.path
        # Redirect to the login page.
        return redirect(url_for('auth.login'))
    if request.method == 'POST':
        data = request.form
        send_email(data['name'], data['email'], data['message'])
        return render_template('contact.html', msg_sent=True)
    # If the user is authenticated, render the contact page.
    return render_template('contact.html')