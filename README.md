# Stock Screener

A Python-based stock screener that automatically identifies bullish trading opportunities in the Nifty 500 index using technical indicators (EMA and MACD). The application fetches historical stock data, evaluates multiple technical indicators, and can send results via email.

## Table of Contents

- [Overview](#overview)
- [Features](#features)
- [Project Structure](#project-structure)
- [Requirements](#requirements)
- [Installation](#installation)
- [Configuration](#configuration)
- [Usage](#usage)
  - [Basic Screening](#basic-screening)
  - [Email Notifications](#email-notifications)
  - [Reproducing Issues](#reproducing-issues)
- [modules](#modules)
  - [screener.py](#screenerpy)
  - [indicators.py](#indicatorspy)
  - [utils.py](#utilspy)
  - [send_email.py](#send_emailpy)
- [Technical Indicators](#technical-indicators)
- [How It Works](#how-it-works)
- [Data Source](#data-source)
- [Error Handling](#error-handling)
- [Dependencies](#dependencies)

## Overview

This stock screener analyzes 500 Indian stocks from the Nifty 500 index to identify potential buying opportunities based on technical analysis. It uses multiple indicators to confirm bullish trends before flagging a stock as positive.

## Features

- **Automated Stock Screening**: Scans all 500 stocks in the Nifty 500 index
- **EMA Analysis**: Evaluates 5, 13, and 21-day Exponential Moving Averages
- **MACD Signals**: Detects bullish crossovers using MACD (Moving Average Convergence Divergence)
- **200-Day EMA**: Confirms long-term trend strength
- **Historical Data Fetching**: Automatically pulls 5 years of historical data from Yahoo Finance
- **Results Formatting**: Generates clean, readable output with relevant indicators
- **Email Notifications**: Sends formatted HTML email reports with screening results
- **Error Handling**: Gracefully handles API failures and data issues
- **MultiIndex Column Handling**: Automatically flattens MultiIndex columns from newer yfinance versions

## Project Structure

```
stock-screener/
├── README.md                          # Project documentation
├── stock_screener/
│   ├── __init__.py                    # Package initialization
│   ├── screener.py                    # Main screening logic
│   ├── indicators.py                  # Technical indicator calculations
│   ├── utils.py                       # Utility functions and helpers
│   ├── version.py                     # Version information
│   ├── config.ini                     # Configuration file (currently empty)
│   ├── requirements.txt                # Python dependencies
│   └── ticker-symbol/
│       └── nifty-500.csv              # List of Nifty 500 stock symbols
├── reproduce_issue.py                 # Issue reproduction script
└── send_email.py                      # Email sending functionality
```

## Requirements

- Python 3.7+
- Internet connection (for fetching stock data)
- Gmail account with App Password (for email functionality)

## Installation

1. **Clone or navigate to the project directory**:
   ```bash
   cd stock-screener
   ```

2. **Create a virtual environment** (recommended):
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. **Install dependencies**:
   ```bash
   pip install -r stock_screener/requirements.txt
   ```

## Configuration

### Email Setup

To use the email notification feature, set the following environment variables:

```bash
export USER_EMAIL="your-gmail@gmail.com"
export USER_PASSWORD="your-app-password"
```

**Note**: Use Gmail [App Passwords](https://support.google.com/accounts/answer/185833), not your regular password.

### Nifty 500 List

The screener uses `stock_screener/ticker-symbol/nifty-500.csv` containing stock symbols. This CSV file must have a 'Symbol' column with stock ticker names (without the ".NS" suffix, which is added automatically).

## Usage

### Basic Screening

Run the stock screener to identify bullish stocks:

```bash
python -m stock_screener.screener
```

This will:
1. Load all Nifty 500 stock symbols from the CSV file
2. Fetch 5 years of historical data for each stock
3. Evaluate EMA and MACD indicators
4. Return a Pandas DataFrame with all positive stocks
5. Print results to console

**Example Output**:
```
SCREENER RUNNING
   Stock Name    ema_5    ema_13    ema_21          MACD      Signal   Histogram    ema_200
0  RELIANCE.NS  2345.67  2340.12  2335.89      12.345    11.234        1.111      2200.00
```

### Email Notifications

Send screening results via email:

```bash
python send_email.py
```

This will:
1. Run the stock screener
2. Format results into an HTML table
3. Send a styled HTML email to configured recipients

The email includes a nicely formatted HTML table with all the screened stock data.

## Modules

### screener.py

**Main screening orchestrator**

- `evaluate_stock(ticker, periods)`: Evaluates a single stock
  - Fetches historical data
  - Checks EMA and MACD conditions
  - Returns positive/negative status with indicator values
  - Default period: 5 years

- `screener()`: Screens all Nifty 500 stocks
  - Iterates through all symbols
  - Handles errors gracefully
  - Returns formatted DataFrame of positive stocks

### indicators.py

**Technical indicator calculations**

- `calculate_ema(data, time_window)`: Calculates Exponential Moving Average
  - Returns last 5 days of EMA values
  - Supports any time window (5, 13, 21, 200, etc.)

- `calculate_macd(data)`: Calculates MACD indicators
  - EMA(12) - EMA(26) = MACD line
  - Signal = EMA(9) of MACD
  - Histogram = MACD - Signal
  - Returns DataFrame with all three values

### utils.py

**Utility functions**

- `fetch_stock_data(ticker, periods)`: Downloads historical data from Yahoo Finance
  - Handles MultiIndex column flattening
  - Filters data by date range
  - Default: 1 year of data

- `evaluate_ema(data)`: Checks if EMA is bullish
  - Condition: EMA(5) > EMA(13) AND EMA(5) > EMA(21)
  - Returns boolean + EMA values

- `evaluate_macd(data)`: Checks for bullish MACD crossover
  - Condition: Histogram[-1] > 0 AND Histogram[-2] < 0 (bullish crossover)
  - Returns boolean + MACD DataFrame

- `format_positive_stocks(positive_stocks)`: Formats screening results
  - Flattens nested dictionaries
  - Creates clean Pandas DataFrame
  
- `calculate_200_days_ema(data)`: Calculates 200-day EMA for trend confirmation

- `calculate_cagr(beginning_value, ending_value, num_years)`: Compound Annual Growth Rate
  - Formula: ((ending/beginning)^(1/years) - 1) * 100

- `calculate_percent_change(old_value, new_value)`: Percentage change calculation
  - Formula: ((new - old) / old) * 100

- `calculate_rolling_return(data, window)`: Rolling window returns analysis
  - Computes CAGR and percent change for rolling periods

- `plot_rolling_returns(returns_df)`: Visualizes rolling returns with matplotlib

### send_email.py

**Email notification functionality**

- Runs the stock screener
- Formats results using pretty-html-table library
- Sends styled HTML email via Gmail SMTP
- Recipients: Configured via 'Bcc' field
- Requires: USER_EMAIL and USER_PASSWORD environment variables

## Technical Indicators

### EMA (Exponential Moving Average)

An EMA gives more weight to recent prices. The screener uses three EMAs:
- **5-day EMA**: Fast-moving average (most responsive to recent changes)
- **13-day EMA**: Medium-term trend
- **21-day EMA**: Slower trend confirmation
- **200-day EMA**: Long-term trend strength

**Bullish Condition**: EMA(5) > EMA(13) AND EMA(5) > EMA(21)

### MACD (Moving Average Convergence Divergence)

MACD is a momentum indicator that shows the relationship between two moving averages:

- **MACD Line**: EMA(12) - EMA(26)
- **Signal Line**: EMA(9) of MACD line
- **Histogram**: MACD - Signal (visual representation of difference)

**Bullish Signal**: MACD Histogram crosses above zero (from negative to positive)
- This indicates momentum is shifting from bearish to bullish
- Condition checked: Histogram[-1] > 0 AND Histogram[-2] < 0

## How It Works

1. **Data Fetch**: Retrieves 5 years of historical price data for each stock
2. **Indicator Calculation**: Computes EMA and MACD values
3. **Validation**: Checks both indicators are bullish
4. **Confirmation**: Ensures 200-day EMA is above current price (long-term trend)
5. **Aggregation**: Collects all positive stocks
6. **Formatting**: Returns results in a clean DataFrame format
7. **Notification**: Optionally sends results via email

## Data Source

Stock data is fetched from **Yahoo Finance** via the `yfinance` library:
- Data range: 5 years historical data
- Update frequency: Real-time (when screener runs)
- Ticker format: Uses ".NS" suffix for NSE (National Stock Exchange) listings
  - Example: "RELIANCE" → "RELIANCE.NS"

## Error Handling

The screener includes robust error handling:

- **API Failures**: Catches yfinance errors and continues to next stock
- **Data Issues**: Handles missing or incomplete data gracefully
- **MultiIndex Columns**: Automatically flattens newer yfinance column structures
- **Network Errors**: Exception handling with informative error messages

Each failed stock logs an error message but doesn't stop the screening process.

## Dependencies

| Package | Purpose |
|---------|---------|
| `yfinance` | Yahoo Finance data fetching |
| `pandas` | Data manipulation and analysis |
| `pretty-html-table` | HTML table formatting for emails |
| `python-dateutil` | Date/time handling |
| `pytz` | Timezone support |
| `six` | Python 2/3 compatibility |
| `tzdata` | Timezone database |
| `matplotlib` | Data visualization (rolling returns plotting) |

Install all dependencies at once:
```bash
pip install -r stock_screener/requirements.txt
```

## Troubleshooting

### Issue: yfinance returns MultiIndex columns

**Solution**: The code automatically handles this in `fetch_stock_data()`. Test with:
```bash
python reproduce_issue.py
```

### Issue: Email not sending

- Verify environment variables are set: `USER_EMAIL`, `USER_PASSWORD`
- Ensure Gmail App Password is used (not regular password)
- Check Gmail security settings allow SMTP access

### Issue: No stocks returned after screening

- Verify internet connection
- Check that nifty-500.csv is in correct location
- Run `reproduce_issue.py` to verify data fetching works
- Check console for specific error messages
