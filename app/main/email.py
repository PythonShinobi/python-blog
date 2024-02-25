
import os
import smtplib
from threading import Thread
from email.mime.text import MIMEText
from dotenv import load_dotenv

ENV = '.env'
load_dotenv(ENV)

# Fetching SMTP server configuration from environment variables.
SERVER = os.getenv('MAIL_SERVER')
PORT = os.getenv('MAIL_PORT')
EMAIL = os.getenv('ADMIN_EMAIL')
PASSWORD = os.getenv('ADMIN_EMAIL_PASSWORD')

def _email(name, from_addr,  message):
    # Constructing the email message.
    msg = f"Subject: New Message\n\nName: {name}\nEmail: {from_addr}\nMessage: {message}"
    mime_message = MIMEText(msg, 'plain', 'utf-8')

    # Sending the email.
    with smtplib.SMTP(SERVER, PORT) as connection:
        # Initiating a secure connection.
        connection.starttls()
        # Logging in to the SMTP server.
        connection.login(EMAIL, PASSWORD)
        # Sending the email.
        connection.sendmail(from_addr=from_addr, to_addrs=EMAIL, msg=mime_message.as_string())

# Function to send an email in a separate thread.
def send_email(name, from_addr, message):
    # Creating a new thread to send the email.
    thread = Thread(target=_email, args=(name, from_addr, message))
    thread.start()

# Example usage:
# You need to call send_email with appropriate parameters, such as sender's name, email, and message.
# The sender's email address should be provided as from_addr.