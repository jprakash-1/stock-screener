import smtplib
import ssl
import os
import json  # Add this import for JSON formatting
import pandas as pd
from stock_screener.screener import screener
import polars as pl

with pl.Config() as cfg:
    cfg.set_fmt_str_lengths(50)

port = 465
smtp_server = "smtp.gmail.com"
USERNAME = os.environ.get('USER_EMAIL')
PASSWORD = os.environ.get('USER_PASSWORD')

formatted_string = screener()

# Email content
message = f"Stock Data:\n\n{formatted_string}"

context = ssl.create_default_context()
with smtplib.SMTP_SSL(smtp_server, port, context=context) as server:
    server.login(USERNAME, PASSWORD)
    # Replace USERNAME with the recipient's email address
    server.sendmail(USERNAME, USERNAME, message)