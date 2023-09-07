import os
import json
import numpy as np
import pandas as pd
from stock_screener.utils import evaluate_ema, evaluate_macd, calculate_200_days_ema

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

    if ema_flag and macd_flag: 
        positive_stock[ticker]["ema_5"] = ema_record[0]
        positive_stock[ticker]["ema_13"] = ema_record[1]
        positive_stock[ticker]["ema_21"] = ema_record[2]
        positive_stock[ticker]['macd'] = macd_record.to_dict("records")

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
    for ticker in NIFTY_500_tickers[:100]:
        print(ticker)
        try:
            ticker = ticker + ".NS"
            period = "6mo"
            stock_sentiment, stock_info = evaluate_stock(ticker, period)
            ema_200 = calculate_200_days_ema(ticker, period = "5y")
            stock_info['ema_200'] = ema_200
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
