# app.py
import streamlit as st
import pandas as pd
from utils import fetch_stock_data, calculate_rolling_return, plot_rolling_returns


page_bg_img = f"""
<style>
[data-testid="stAppViewContainer"] > .main {{
background-image: url("https://images.unsplash.com/photo-1501426026826-31c667bdf23d");
background-size: 180%;
background-position: top left;
background-repeat: no-repeat;
background-attachment: local;
}}


[data-testid="stHeader"] {{
background: rgba(0,0,0,0);
}}

[data-testid="stToolbar"] {{
right: 2rem;
}}
</style>
"""

st.markdown(page_bg_img, unsafe_allow_html=True)

st.title("My Streamlit App")

# Add a text input widget
ticker_symbol = st.text_input("Enter stock symbol", "TATAMOTORS")
if ticker_symbol:
    stock_data = fetch_stock_data(ticker_symbol +".NS",5)
    stock_rolling_returns = calculate_rolling_return(stock_data, window = 252)
    returns_df = pd.DataFrame(stock_rolling_returns).iloc[::-1].reset_index().drop(['index'], axis = 1)
    fig =  plot_rolling_returns(returns_df)
    st.plotly_chart(fig)
else:
    st.write("Please enter stock_symbol")

