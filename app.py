# Import libraries
import yfinance as yf
import plotly.graph_objects as go
import streamlit as st
from datetime import datetime

# Function to fetch real-time stock data
def fetch_realtime_data(stock_symbol):
    data = yf.download(stock_symbol, period="1d", interval="1m")
    return data

# Function to detect chart patterns
def detect_chart_patterns(data):
    patterns = []
    for i in range(2, len(data) - 2):
        # Detect Head and Shoulders
        left_shoulder = data['High'][i - 1] > data['High'][i - 2] and data['High'][i - 1] > data['High'][i]
        head = data['High'][i] > data['High'][i - 1] and data['High'][i] > data['High'][i + 1]
        right_shoulder = data['High'][i + 1] > data['High'][i] and data['High'][i + 1] > data['High'][i + 2]
        
        if left_shoulder and head and right_shoulder:
            patterns.append((data.index[i], 'Head and Shoulders'))
    
    return patterns

# Streamlit app
def main():
    st.title("Real-Time Stock Chart Pattern Detection")
    
    # User input: Stock symbol
    stock_symbol = st.text_input("Enter Stock Symbol (e.g., AAPL):", "AAPL")
    
    # Fetch real-time data
    data = fetch_realtime_data(stock_symbol)
    
    # Plot candlestick chart
    fig = go.Figure(data=[go.Candlestick(
        x=data.index,
        open=data['Open'],
        high=data['High'],
        low=data['Low'],
        close=data['Close']
    )])
    st.plotly_chart(fig)
    
    # Detect and notify patterns
    patterns = detect_chart_patterns(data)
    for pattern in patterns:
        st.warning(f"Alert: {pattern[1]} detected at {pattern[0]}!")

# Run the app
if __name__ == "__main__":
    main()

