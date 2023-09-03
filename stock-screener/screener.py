import numpy as np
import pandas as pd
from utils import evaluate_ema, evaluate_macd

def evaluate_stock(ticker, period = "6mo"):
    """_summary_

    Args:
        ticker (_type_): _description_
        period (str, optional): _description_. Defaults to "6mo".

    Returns:
        _type_: _description_
    """
    positive_stock = {}
    positive_stock[ticker] = {}
    ema_flag, ema_record = evaluate_ema(ticker, period) 
    macd_flag, macd_record = evaluate_macd(ticker, period)

    if ema_flag and macd_flag: 
        positive_stock[ticker]["ema_5"] = ema_5
        positive_stock[ticker]["ema_13"] = ema_13
        positive_stock[ticker]["ema_21"] = ema_21
        positive_stock[ticker]['macd'] = macd_record.to_dict("records")

        return True, positive_stock
    return False, {}

def screener():
    """_summary_
    """
    nifty500_df = pd.read_csv("ticker-symbol\nifty-500.csv")
    NIFTY_500_ticker = list(nifty500_df['Symbol'])

    for ticker in NIFTY_500_tickers:
        ticker = ticker + ".NS"
        period = "6mo"
        stock_sentiment, stock_info = evaluate_stock(ticker, period)
        if stock_sentiment: 
            print(stock_info)
        
    print("Completed Stock screening.")

if __name__ == "__main__":
    screener()