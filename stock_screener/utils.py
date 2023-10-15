"""Utilities functions."""
import pandas as pd 
import numpy as np
import yfinance as yf
from datetime import datetime, timedelta

from stock_screener.indicators import calculate_macd, calculate_ema


def evaluate_macd(data):
    """Evaluate MACD for a given stock ticker.

    Args:
        ticker (str): The stock ticker symbol.
        period (str, optional): The data retrieval period. Defaults to "6mo".

    Returns:
        tuple: A tuple containing a boolean value indicating whether MACD is bullish,
               and a DataFrame with MACD data for the last 5 days.
    """
    macd_df = calculate_macd(data)
    hist = macd_df.tail()['Histogram']
    if hist[-1] > 0 and hist[-2] < 0:
        return True, macd_df.tail()
    return False, None

def evaluate_ema(data):
    """Evaluate EMA for a given stock ticker.

    Args:
        ticker (str): The stock ticker symbol.
        period (str, optional): The data retrieval period. Defaults to "6mo".

    Returns:
        tuple: A tuple containing a boolean value indicating whether EMA is bullish,
               and a list of EMA values for the time windows (5, 13, and 21).
    """
    ema_5 = calculate_ema(data, time_window=5)
    ema_13 = calculate_ema(data, time_window=13)
    ema_21 = calculate_ema(data, time_window=21)

    if ema_5[-1] > ema_13[-1] and ema_5[-1] > ema_21[-1]:
        return True, [ema_5, ema_13, ema_21]
    return False, []

def format_positive_stocks(positive_stocks):
    """Format the screened stocks.

    Args:
        positive_stocks (List[Dict[str,Any]]): _description_

    Returns:
        List[Dict[str,Any]]: _description_
    """
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

def calculate_200_days_ema(data):
    """Calculate Exponential Moving average for a given stock.

    Args:
        ticker (str): The stock ticker symbol.
        period (str, optional): The data retrieval period. Defaults to "5y".

    Returns:
        Stock 200 days exponential moving average price.
    """
    ema_200 =  calculate_ema(data, time_window=200)

    return ema_200

def fetch_stock_data(ticker, periods = 1):
    try:
        today = datetime.now()
        start_date = today - timedelta(days = 365 * periods)
        end_date = today.strftime('%Y-%m-%d')
        
        # Download historical stock data from Yahoo Finance
        half_decade_stock_data = yf.download(ticker, period= str(periods)+"y")
        stock_data = half_decade_stock_data.loc[(half_decade_stock_data.index >= start_date) & (half_decade_stock_data.index <= end_date)]
        return stock_data
    except Exception as e:
        print(f"Error fetching data for {ticker}: {e}")
        return None


