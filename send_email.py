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

def format_dataframe_with_boundaries(df):
    # Step 1: Create a list of column names and set a fixed width of 30 characters for each column
    column_widths = [25] * len(df.columns)

    # Step 2: Create a separator line with cell boundaries
    separator = '+'.join(['.' * (width + 10) for width in column_widths])

    # Step 3: Initialize the output string with headers and separator
    output = separator + '\n'
    
    # Step 4: Format column headers using a for loop
    headers = '|'
    for col, width in zip(df.columns, column_widths):
        # Check if the column contains numeric values (int or float)
        if df[col].dtype in ['int64', 'float64']:
            # Format numeric column headers as centered with the specified width
            formatted_header = f"{col: ^{width}}".center(width)
        else:
            # Format non-numeric column headers as left-aligned with the specified width
            formatted_header = f"{col: <{width}}".center(width)
        headers += f" {formatted_header} |"
    headers += '\n'
    output += headers
    output += separator + '\n'

    # Step 5: Iterate through DataFrame rows and add data with cell boundaries and proper alignment
    for _, row in df.iterrows():
        row_data = []
        for col, width in zip(df.columns, column_widths):
            cell_value = str(row[col])
            # Calculate the number of spaces to add to reach the desired width
            spaces_to_add = width - len(cell_value)
            # Format cell values with additional spaces to achieve the desired width
            formatted_value = f"{cell_value}{' ' * spaces_to_add}"
            row_data.append(formatted_value)
        output += '| ' + ' | '.join(row_data) + ' |\n'
        output += separator + '\n'

    return output



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
            
            df_list.append([stock_symbol,  macd, signal, histogram, ema_5, ema_13, ema_21])

# Create the DataFrame
columns = ["Stock Symbol", "MACD", "Signal", "Histogram", "EMA_5", "EMA_13", "EMA_21" ]
df = pd.DataFrame(df_list, columns=columns)
formatted_string = format_dataframe_with_boundaries(df)

# Email content
message = f"Stock Data:\n\n{formatted_string}"

context = ssl.create_default_context()
with smtplib.SMTP_SSL(smtp_server, port, context=context) as server:
    server.login(USERNAME, PASSWORD)
    # Replace USERNAME with the recipient's email address
    server.sendmail(USERNAME, USERNAME, message)