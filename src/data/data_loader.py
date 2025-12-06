import yfinance as yf
import pandas as pd
import numpy as np
from datetime import datetime, timedelta
import os


def download_stock_date(ticker, start_date = None, end_date = None, period ="1y"):
    print(f"Downloading data for {ticker}...")

    try:
        if start_date & end_date:
            data = yf.download(ticker, start = start_date, end = end_date, progress = False)
        else:
            data = yf.download(ticker, period = period, progress = false)

        if data.empty:
            raise ValueError(f"No data found for ticker {ticker}")

        data = data.reset_index()
        
        print(f"✓ Downloaded {len(data)} days of data for {ticker}")
        print(f"  Date range: {data['Date'].min()} to {data['Date'].max()}")

        return data

    except Exception as e:
        print(f"Error downloading data for {ticker}")
        return None

def clean_stock_data(data):
    df = data.copy()
    df = df.dropna()
    df = df.sort_values('Date').reset_index(drop=True)

    columns_to_keep = ['Date', 'Open', 'High','Low', 'Close', 'Volume']
    df = df[columns_to_keep]

    return df

def get_close_prices(data):
    return data['Close'].values

def save_stock_data(data, ticker, folder='data/raw'):
    os.makedirs(folder,exist_ok=True)

    today=datetime.now().strftime(%Y%m%d)
    filename=f"{ticker}_{today}.csv"
    filepath = os.path.join(folder, filename)
    
    data.to_csv(filepath, index=False)
    
    print(f"Saved data to {filepath}")
    
    return filepath

def get_stock_data_for_training(ticker,period='1y',save=True):
    
    data = download_stock_date(ticker,period=period)
    data = clean_stock_data(data)
    close_prices = get_close_prices(data)

    if save:
        save_stock_data(data,ticker)
    
    return data, close_prices