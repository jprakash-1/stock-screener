"""Utilities functions."""
import pandas as pd 
import numpy as np
import yfinance as yf
import polars as pl

from stock_screener.indicators import calculate_macd, calculate_ema

with pl.Config() as cfg:
    cfg.set_fmt_str_lengths(50)

def evaluate_macd(ticker, period="6mo"):
    """Evaluate MACD for a given stock ticker.

    Args:
        ticker (str): The stock ticker symbol.
        period (str, optional): The data retrieval period. Defaults to "6mo".

    Returns:
        tuple: A tuple containing a boolean value indicating whether MACD is bullish,
               and a DataFrame with MACD data for the last 5 days.
    """
    macd_df = calculate_macd(ticker, period=period)
    hist = macd_df.tail()['Histogram']
    if hist[-1] > 0 and hist[-2] < 0:
        return True, macd_df.tail()
    return False, None

def evaluate_ema(ticker, period="6mo"):
    """Evaluate EMA for a given stock ticker.

    Args:
        ticker (str): The stock ticker symbol.
        period (str, optional): The data retrieval period. Defaults to "6mo".

    Returns:
        tuple: A tuple containing a boolean value indicating whether EMA is bullish,
               and a list of EMA values for the time windows (5, 13, and 21).
    """
    ema_5 = calculate_ema(ticker, time_window=5, period=period)
    ema_13 = calculate_ema(ticker, time_window=13, period=period)
    ema_21 = calculate_ema(ticker, time_window=21, period=period)

    if ema_5[-1] > ema_13[-1] and ema_5[-1] > ema_21[-1]:
        return True, [ema_5, ema_13, ema_21]
    return False, []

def format_positive_stocks(positive_stocks):
    screened_stocks = []
    for positive_stock in positive_stocks:
        output_dict = {}
        stock_name = list(positive_stock.keys())[0]
        output_dict[stock_name] = {}
        for key, value in positive_stock[stock_name].items():
            if key != "macd":
                output_dict[stock_name][key] = value
            elif key == "macd":
                for macd_key, macd_value in value.items():
                    output_dict[stock_name][macd_key] = macd_value
        screened_stocks.append(output_dict)

    new_data = []
    for screened_stock in screened_stocks:
        stock_name, value = list(screened_stock.items())[0]
        value['Stock Name'] = stock_name
        new_data.append(value)

    output_message = pd.DataFrame(new_data)

    return output_message

def calculate_200_days_ema(ticker, period = "5y"):
    """_summary_

    Args:
        ticker (_type_): _description_
        period (str, optional): _description_. Defaults to "2y".
    """
    ema_200 =  calculate_ema(ticker, time_window=5, period=period)

    return ema_200


def format_dataframe_with_boundaries(df):
    # Step 1: Create a list of column names and set a fixed width of 30 characters for each column
    column_widths = [25] * len(df.columns)

    # Step 2: Create a separator line with cell boundaries
    separator = '+'.join(['-' * (width) for width in column_widths])

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