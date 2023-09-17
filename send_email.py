import smtplib
import ssl
import os
import json  # Add this import for JSON formatting
import pandas as pd
from pretty_html_table import build_table
from stock_screener.screener import screener
from email.message import EmailMessage

port = 465
smtp_server = "smtp.gmail.com"
USERNAME = os.environ.get('USER_EMAIL')
PASSWORD = os.environ.get('USER_PASSWORD')

formatted_df = screener()

body = """
<html>
<head>
</head>

<body>
Hi,

<br><br>

Please find the screener report 
        {0}
</body>

</html>
""".format(
    build_table(
        formatted_df,
        "blue_light",
        width="auto",
        font_family="Open Sans",
        font_size="13px",
        text_align="justify",
    )
)
message = EmailMessage()

# Email info
message['To'] = USERNAME
message['From'] = USERNAME
message['Subject'] = "Stock Screener"
message.add_alternative(body, subtype="html")

context = ssl.create_default_context()
with smtplib.SMTP_SSL(smtp_server, port, context=context) as server:
    server.login(USERNAME, PASSWORD)
    # Replace USERNAME with the recipient's email address
    server.send_message(message)