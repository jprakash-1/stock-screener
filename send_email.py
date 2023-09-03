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
        ema_5 = round(stock_info["ema_5"], 2)
        ema_13 = round(stock_info["ema_13"], 2)
        ema_21 = round(stock_info["ema_21"], 2)
        macd_data = stock_info["macd"]

        for i, macd_entry in enumerate(macd_data):
            macd = round(macd_entry["MACD"], 2)
            signal = round(macd_entry["Signal"], 2)
            histogram = round(macd_entry["Histogram"], 2)

            if i == 0:
                df_list.append([stock_symbol,  macd, signal, histogram, ema_5, ema_13, ema_21])
            else:
                df_list.append(["-----------",  macd, signal, histogram, "----------" , "----------", "----------"])

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