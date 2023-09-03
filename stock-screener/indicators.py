"""Indicators logic."""
import pandas as pd
import numpy as np
import yfinance as yf

def calculate_macd(ticker, period):
    """_summary_

    Args:
        ticker (_type_): _description_
        period (_type_): _description_

    Returns:
        _type_: _description_
    """
    # get the stock data from Yahoo Finance
    data = yf.download(ticker, period=period)
    # calculate the 12-day EMA
    ema_12 = data['Close'].ewm(span=12, adjust=False).mean()
    # calculate the 26-day EMA
    ema_26 = data['Close'].ewm(span=26, adjust=False).mean()
    # calculate the MACD line
    macd = ema_12 - ema_26
    # calculate the 9-day EMA of MACD
    signal = macd.ewm(span=9, adjust=False).mean()
    # calculate the MACD histogram
    histogram = macd - signal
    # create a DataFrame with MACD, signal, and histogram
    macd_df = pd.DataFrame({'MACD': macd, 'Signal': signal, 'Histogram': histogram})
    return macd_df

def calculate_ema(ticker, period = "6mo"):
    """_summary_

    Args:
        ticker (_type_): _description_
        period (str, optional): _description_. Defaults to "6mo".

    Returns:
        _type_: _description_
    """
    ticker = ticker + ".NS"
    data = yf.Ticker(ticker).history(period="6mo")
    ema_5 = data['Close'].rolling(5).mean()
    ema_13 = data['Close'].rolling(13).mean()
    ema_21 = data['Close'].rolling(21).mean()

    return ema_5, ema_13, ema_21

