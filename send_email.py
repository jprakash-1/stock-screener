import smtplib
import ssl
import os
import json  # Add this import for JSON formatting
import pandas as pd
from stock_screener.screener import screener
from email.message import EmailMessage

port = 465
smtp_server = "smtp.gmail.com"
USERNAME = os.environ.get('USER_EMAIL')
PASSWORD = os.environ.get('USER_PASSWORD')

formatted_string = screener()
message = EmailMessage()

# Email info
message.set_content(f"Stock Data:\n\n{formatted_string}") 
message['To'] = USERNAME
message['From'] = USERNAME
message['Subject'] = "Stock Screener"

context = ssl.create_default_context()
with smtplib.SMTP_SSL(smtp_server, port, context=context) as server:
    server.login(USERNAME, PASSWORD)
    # Replace USERNAME with the recipient's email address
    server.send_message(message)