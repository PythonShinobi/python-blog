
from flask import current_app, render_template
from flask_mail import Message
from threading import Thread

from app import mail

def _send_async_email(flask_app, msg):
    # Create an application context for the thread.
    with flask_app.app_context():
        mail.send(msg)

def send_email(subject, sender, recipients, text_body, html_body):
    msg = Message(subject=subject, sender=sender, recipients=recipients)
    msg.body = text_body
    msg.html = html_body
    # Sending the email in a separate thread allows the main thread of the Flask application to continue 
    # handling other requests or tasks without waiting for the email sending process to complete.
    Thread(target=_send_async_email, args=(current_app._get_current_object(), msg)).start()

# The application, acting on behalf of the administrator sends the password reset email 
# to the specified user's email address.
def send_password_reset_email(user):
    """Send a token to reset the user's password through their email."""
    token = user.get_reset_password_token()  # Generate a reset password token for the user.
    send_email(
        subject=('Reset Your Password'),
        sender=current_app.config['ADMIN'][0],
        recipients=[user.email],
        text_body=render_template('email/reset_password.txt', user=user, token=token),
        html_body=render_template('email/reset_password.html', user=user, token=token)
    )