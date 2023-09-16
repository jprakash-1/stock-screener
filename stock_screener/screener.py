import os
import json
import numpy as np
import pandas as pd
from stock_screener.utils import evaluate_ema, evaluate_macd, calculate_200_days_ema, format_positive_stocks
import polars as pl

with pl.Config() as cfg:
    cfg.set_fmt_str_lengths(50)

def evaluate_stock(ticker, period = "6mo"):
    """Evaluate stock based on EMA and MACD indicators.

    Args:
        ticker (str): The stock ticker symbol.
        period (str, optional): The evaluation period (e.g., "6mo"). Defaults to "6mo".

    Returns:
        tuple: A tuple containing a boolean indicating if the stock is positive based on EMA and MACD,
               and a dictionary containing EMA and MACD information.
    """
    positive_stock = {}
    positive_stock[ticker] = {}
    ema_flag, ema_record = evaluate_ema(ticker, period) 
    macd_flag, macd_record = evaluate_macd(ticker, period)
    ema_200 = calculate_200_days_ema(ticker, period = "5y")

    if ema_flag and macd_flag: 
        positive_stock[ticker]["ema_5"] = ema_record[0][-1]
        positive_stock[ticker]["ema_13"] = ema_record[1][-1]
        positive_stock[ticker]["ema_21"] = ema_record[2][-1]
        positive_stock[ticker]['macd'] = macd_record.to_dict("records")[-1]
        positive_stock[ticker]["ema_200"] = ema_200[-1]
        print(ema_200)
    
        return True, positive_stock
    return False, {}

def screener():
    """Screen stocks in the Nifty 500 and identify positive stocks based on EMA and MACD indicators.

    Returns:
        list: A list of dictionaries, where each dictionary contains information about a positive stock.
    """
    nifty500_file_path = "stock_screener/ticker-symbol/nifty-500.csv"
    nifty500_df = pd.read_csv(nifty500_file_path)
    NIFTY_500_tickers = list(nifty500_df['Symbol'])

    all_positive_stock_info = []
    for ticker in NIFTY_500_tickers[:50]:
        print(ticker)
        # try:
        ticker = ticker + ".NS"
        period = "1y"
        stock_sentiment, stock_info = evaluate_stock(ticker, period)
        if stock_sentiment: 
            all_positive_stock_info.append(stock_info)
        # except: 
        #     print("exception")        
    print("Completed Stock screening.")
    return format_positive_stocks(all_positive_stock_info)

if __name__ == "__main__":
    print("SCREENER RUNNING")
    all_positive_stock_info = screener()

    print(all_positive_stock_info)