import os
import json
import numpy as np
import pandas as pd
from stock_screener.utils import evaluate_ema, evaluate_macd

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
        positive_stock[ticker]["ema_5"] = ema_record[0]
        positive_stock[ticker]["ema_13"] = ema_record[1]
        positive_stock[ticker]["ema_21"] = ema_record[2]
        positive_stock[ticker]['macd'] = macd_record.to_dict("records")

        return True, positive_stock
    return False, {}

def screener():
    """_summary_
    """
    nifty500_file_path = "stock_screener/ticker-symbol/nifty-500.csv"
    nifty500_df = pd.read_csv(nifty500_file_path)
    NIFTY_500_tickers = list(nifty500_df['Symbol'])

    all_positive_stock_info = []
    for ticker in NIFTY_500_tickers[:100]:
        print(ticker)
        try:
            ticker = ticker + ".NS"
            period = "6mo"
            stock_sentiment, stock_info = evaluate_stock(ticker, period)
            if stock_sentiment: 
                all_positive_stock_info.append(stock_info)

        except: 
            print("exception")        
    print("Completed Stock screening.")
    return all_positive_stock_info


# if __name__ == "__main__":
#     all_positive_stock_info = screener()
#     # Convert the list of dictionaries to a JSON-formatted string with indentation
#     formatted_data = json.dumps(all_positive_stock_info, indent=4)
#     print(formatted_data)