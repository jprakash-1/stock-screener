"""Utilities functions."""
import pandas as pd 
import numpy as np
import yfinance as yf

from stock_screener.indicators import calculate_macd, calculate_ema


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
        output_dict[stock_name]['Stock Name'] = stock_name
        for key, value in positive_stock[stock_name].items():
            if key != "macd":
                output_dict[stock_name][key] = value
            elif key == "macd":
                for macd_key, macd_value in value.items():
                    output_dict[stock_name][macd_key] = macd_value
        screened_stocks.append(output_dict[stock_name])
    output_message = pd.DataFrame(screened_stocks)

    return output_message

def calculate_200_days_ema(ticker, period = "5y"):
    """_summary_

    Args:
        ticker (_type_): _description_
        period (str, optional): _description_. Defaults to "2y".
    """
    ema_200 =  calculate_ema(ticker, time_window=5, period=period)

    return ema_200
