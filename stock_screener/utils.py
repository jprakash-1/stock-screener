"""Utilities functions."""
import pandas as pd 
import yfinance as yf
from datetime import datetime, timedelta

import matplotlib.pyplot as plt
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
    if hist.iloc[-1] > 0 and hist.iloc[-2] < 0:
        return True, macd_df.tail()
    return False, None

def evaluate_ema(data):
    """Evaluate EMA for a given stock ticker.

    Args:
        ticker (str): The stock ticker symbol.
        period (str, optional): The data retrieval period. Defaults to "6mo".

    Returns:
        tuple: A tuple containing a boolean value indicating wh ether EMA is bullish,
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
        half_decade_stock_data = yf.download(ticker, period= str(periods)+"y", auto_adjust=True)
        
        # Flatten MultiIndex columns if present (happens with newer yfinance versions)
        if isinstance(half_decade_stock_data.columns, pd.MultiIndex):
            half_decade_stock_data.columns = half_decade_stock_data.columns.get_level_values(0)
            
        stock_data = half_decade_stock_data.loc[(half_decade_stock_data.index >= start_date) & (half_decade_stock_data.index <= end_date)]
        
        if stock_data.empty:
            return None

        return stock_data
    except Exception as e:
        print(f"Error fetching data for {ticker}: {e}")
        return None


def calculate_cagr(beginning_value, ending_value, num_years):
    """
    Calculate the Compound Annual Growth Rate (CAGR).

    Args:
    beginning_value (float): The initial investment or value.
    ending_value (float): The final investment or value.
    num_years (int): The number of years over which the growth occurred.

    Returns:
    float: The CAGR as a percentage.
    """
    # Calculate the CAGR formula
    cagr = ((ending_value / beginning_value) ** (1 / num_years)) - 1

    # Convert to a percentage
    cagr_percentage = cagr * 100

    return cagr_percentage

def calculate_percent_change(old_value, new_value):
    """
    Calculate the percent change between an old value and a new value.

    Args:
    old_value (float): The initial value.
    new_value (float): The final value.

    Returns:
    float: The percent change as a percentage.
    """
    percent_change = ((new_value - old_value) / old_value) * 100
    return percent_change
    
def get_datetime_info(date_range):
  start_date = pd.to_datetime(date_range.split('|')[0]).strftime('%b-%Y')
  end_date = pd.to_datetime(date_range.split('|')[1]).strftime('%b-%Y')

  return str(start_date) + "\n | \n" + str(end_date)


def calculate_rolling_return(data, window):
  total_traded_days = len(data['Close']) - 1
  stock_rolling_returns = []
  temp_data = data['Close']

  for day in range(0, total_traded_days - window):
    single_iteration_return = {}
    start_idx = total_traded_days - day
    end_idx = total_traded_days - (day + window)

    # Calculate daily returns
    daily_returns = temp_data[start_idx] - temp_data[end_idx]

    ending_value = data.iloc[start_idx]['Close']
    beginning_value = data.iloc[end_idx]['Close']
    # Get the Close prices for the specified date range
    close_prices_end = data.iloc[start_idx:start_idx + 1]['Close'].to_dict()
    close_prices_start = data.iloc[end_idx:end_idx + 1]['Close'].to_dict()
    cagr = calculate_cagr(beginning_value, ending_value, num_years = 3)
    percent_change = calculate_percent_change(beginning_value, ending_value)
    date_range = str(data.iloc[start_idx].name) +"|"+ str(data.iloc[end_idx].name)
    
    single_iteration_return['cagr'] = cagr
    single_iteration_return['percent_change'] = percent_change
    single_iteration_return['date_range'] = date_range
    stock_rolling_returns.append(single_iteration_return)

  return stock_rolling_returns

def plot_rolling_returns(returns_df):
  plt.figure(figsize=(20, 10))
  plt.plot(returns_df['date_range'], returns_df['cagr'], linestyle='-', color='b', markersize=8)

  # Set the x-axis tick locations and labels
  x_ticks = returns_df['date_range'][::84]  # Adjust the interval as needed
  x_labels = [get_datetime_info(date) for date in x_ticks]

  plt.xticks(x_ticks, x_labels)
  plt.xlabel('Date Range')
  plt.ylabel('CAGR')
  plt.title('CAGR Over Time')

  min_cagr = int(returns_df['cagr'].min() // 5) - 2
  max_cagr = int(returns_df['cagr'].max() // 5) + 2
  # Add horizontal lines for specific CAGR values (5, 10, 15, 20)
  for cagr_value in range(min_cagr, max_cagr):
      plt.axhline(y=cagr_value*5, color='r', linestyle='-', linewidth=0.3)

  plt.show()