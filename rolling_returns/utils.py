import pandas as pd 
import yfinance as yf
from datetime import datetime, timedelta
import matplotlib.pyplot as plt
import plotly.express as px
import plotly.graph_objects as go


def fetch_stock_data(ticker, periods = 1):
    try:
        today = datetime.now()
        start_date = today - timedelta(days = 365 * periods)
        end_date = today.strftime('%Y-%m-%d')

        # Download historical stock data from Yahoo Finance
        half_decade_stock_data = yf.download(ticker, period= str(periods)+"y")
        stock_data = half_decade_stock_data.loc[(half_decade_stock_data.index >= start_date) & (half_decade_stock_data.index <= end_date)]
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



def calculate_rolling_return(data, window):
  total_traded_days = len(data['Close']) - 1
  stock_rolling_returns = []
  for day in range(0, total_traded_days - window):
    single_iteration_return = {}
    start_idx = total_traded_days - day
    end_idx = total_traded_days - (day + window)

    ending_value = data.iloc[start_idx]['Close']
    beginning_value = data.iloc[end_idx]['Close']

    cagr = calculate_cagr(beginning_value, ending_value, num_years = 3)
    percent_change = calculate_percent_change(beginning_value, ending_value)
    date_range = str(data.iloc[start_idx].name) +"|"+ str(data.iloc[end_idx].name)
    single_iteration_return['cagr'] = cagr
    single_iteration_return['percent_change'] = percent_change
    single_iteration_return['date_range'] = date_range
    stock_rolling_returns.append(single_iteration_return)
  
  return stock_rolling_returns


def get_datetime_info(date_range):
    start_date = pd.to_datetime(date_range.split('|')[0]).strftime('%b-%Y')
    end_date = pd.to_datetime(date_range.split('|')[1]).strftime('%b-%Y')

    return [start_date, '|', end_date]

def plot_rolling_returns(returns_df):
    # Create a figure using Plotly
    fig = go.Figure()

    # Plot the data
    fig.add_trace(go.Scatter(x=returns_df['date_range'], y=returns_df['cagr'],
                             mode='lines',
                             name='CAGR',
                             line=dict(color='blue', width=2),
                             marker=dict(size=8)))

    # Set the x-axis tick locations and labels
    x_ticks = returns_df['date_range'][::84]  # Adjust the interval as needed
    x_labels = [get_datetime_info(date) for date in x_ticks]

    fig.update_layout(xaxis=dict(tickmode='array', tickvals=x_ticks, ticktext=x_labels,
                      tickangle=0, tickfont=dict(size=10)),
                      xaxis_title='Date Range',
                      yaxis_title='CAGR',
                      title='CAGR Over Time',
                      showlegend=True,
                      )

    min_cagr = int(returns_df['cagr'].min() // 5) - 2
    max_cagr = int(returns_df['cagr'].max() // 5) + 2

    # Add horizontal lines for specific CAGR values (5, 10, 15, 20)
    for cagr_value in range(min_cagr, max_cagr):
        fig.add_shape(type="line",
                      x0=returns_df['date_range'].min(),
                      x1=returns_df['date_range'].max(),
                      y0=cagr_value * 5,
                      y1=cagr_value * 5,
                      line=dict(color='green', width=1, dash='dot'))

    return fig