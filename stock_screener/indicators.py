import pandas as pd
import yfinance as yf

def calculate_macd(ticker, period):
    """Calculate MACD (Moving Average Convergence Divergence) indicators for a given stock.

    Args:
        ticker (str): The stock symbol or ticker.
        period (str): The data retrieval period (e.g., "1y" for 1 year, "3mo" for 3 months).

    Returns:
        pandas.DataFrame: A DataFrame containing MACD, Signal, and Histogram values.
    """
    # Get the stock data from Yahoo Finance
    data = yf.download(ticker, period=period)
    # Calculate the 12-day EMA
    ema_12 = data['Close'].ewm(span=12, adjust=False).mean()
    # Calculate the 26-day EMA
    ema_26 = data['Close'].ewm(span=26, adjust=False).mean()
    # Calculate the MACD line
    macd = ema_12 - ema_26
    # Calculate the 9-day EMA of MACD
    signal = macd.ewm(span=9, adjust=False).mean()
    # Calculate the MACD histogram
    histogram = macd - signal
    # Create a DataFrame with MACD, Signal, and Histogram
    macd_df = pd.DataFrame({'MACD': macd, 'Signal': signal, 'Histogram': histogram})
    return macd_df

def calculate_ema(ticker, time_window, period="6mo"):
    """Calculate Exponential Moving Average (EMA) for a given stock.

    Args:
        ticker (str): The stock symbol or ticker.
        time_window (int): The time window for EMA calculation.
        period (str, optional): The data retrieval period (e.g., "1y" for 1 year, "3mo" for 3 months).
            Defaults to "6mo".

    Returns:
        float: The EMA value for the specified time window.
    """
    data = yf.Ticker(ticker).history(period=period)
    ema = data['Close'].ewm(span=time_window, adjust=False).mean()

    return ema.iloc[-5:].values
