"""Utilities functions."""
import pandas as pd 
import numpy as np
import yfinance as yf

from indicators import calculate_macd, calculate_ema


def evaluate_macd(ticker, period = "6mo"):
    """_summary_

    Args:
        ticker (_type_): _description_
        period (str, optional): _description_. Defaults to "6mo".

    Returns:
        _type_: _description_
    """
    macd_df = calculate_macd(ticker, period= period)
    hist = macd_df.tail()['Histogram']
    if hist[-1] > 0 and hist[-2] < 0:
        return True, macd_df.tail()
    
    return False, None

def evaluate_ema(ticker, period = "6mo"):
    """_summary_

    Args:
        ticker (_type_): _description_
        period (str, optional): _description_. Defaults to "6mo".

    Returns:
        _type_: _description_
    """
    ema_5 = evaluate_ema(ticker, time_window = 5, period = period)
    ema_13 = evaluate_ema(ticker, time_window = 13, period = period)
    ema_21 = evaluate_ema(ticker, time_window = 21, period = period)

    if ema_5 > ema_13 and ema_5 > ema_21: 
        return True, [ema_5, ema_13, ema_21]
    return False, []    