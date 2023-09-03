import smtplib
import ssl
import os
import json  # Add this import for JSON formatting
import pandas as pd
from stock_screener.screener import screener

port = 465
smtp_server = "smtp.gmail.com"
USERNAME = os.environ.get('USER_EMAIL')
PASSWORD = os.environ.get('USER_PASSWORD')

all_positive_stock_info = screener()

# Convert JSON data to a pandas DataFrame
df_list = []
for item in all_positive_stock_info:
    for stock_symbol, stock_info in item.items():
        ema_5 = stock_info["ema_5"]
        ema_13 = stock_info["ema_13"]
        ema_21 = stock_info["ema_21"]
        macd_data = stock_info["macd"]

        for macd_entry in macd_data:
            df_list.append([stock_symbol, ema_5, ema_13, ema_21, macd_entry["MACD"], macd_entry["Signal"], macd_entry["Histogram"]])

# Create the DataFrame
columns = ["Stock Symbol", "EMA_5", "EMA_13", "EMA_21", "MACD", "Signal", "Histogram"]
df = pd.DataFrame(df_list, columns=columns)

# Email content
message = f"Stock Data:\n\n{df.to_string(index=False)}"

context = ssl.create_default_context()
with smtplib.SMTP_SSL(smtp_server, port, context=context) as server:
    server.login(USERNAME, PASSWORD)
    # Replace USERNAME with the recipient's email address
    server.sendmail(USERNAME, USERNAME, message)