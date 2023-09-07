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

    if ema_5 > ema_13 and ema_5 > ema_21:
        return True, [ema_5, ema_13, ema_21]
    return False, []

def calculate_200_days_ema(ticker, period = "5y"):
    """_summary_

    Args:
        ticker (_type_): _description_
        period (str, optional): _description_. Defaults to "2y".
    """
    ema_200 =  calculate_ema(ticker, time_window=5, period=period)

    return ema_200