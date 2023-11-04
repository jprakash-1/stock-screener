import pandas as pd
from stock_screener.utils import evaluate_ema, evaluate_macd, calculate_200_days_ema, format_positive_stocks, fetch_stock_data

def evaluate_stock(ticker, periods = 1):
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
 
    stock_data = fetch_stock_data(ticker, periods = periods)

    ema_flag, ema_record = evaluate_ema(stock_data) 
    macd_flag, macd_record = evaluate_macd(stock_data)
    ema_200 = calculate_200_days_ema(stock_data)

    if ema_flag and macd_flag: 
        positive_stock[ticker]["ema_5"] = ema_record[0][-1]
        positive_stock[ticker]["ema_13"] = ema_record[1][-1]
        positive_stock[ticker]["ema_21"] = ema_record[2][-1]
        positive_stock[ticker]['macd'] = macd_record.to_dict("records")[-1]
        positive_stock[ticker]["ema_200"] = ema_200[-1]
    
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
    for ticker in NIFTY_500_tickers:
        try:
            ticker = ticker + ".NS"
            periods = 5
            stock_sentiment, stock_info = evaluate_stock(ticker, periods)
            if stock_sentiment: 
                all_positive_stock_info.append(stock_info)
        except Exception as e:
          print(f"Error fetching data for {ticker}: {e}")        
    print("Completed Stock screening.")
    return format_positive_stocks(all_positive_stock_info)

if __name__ == "__main__":
    print("SCREENER RUNNING")
    all_positive_stock_info = screener()

    print(all_positive_stock_info)