import os
import numpy as np
import yfinance as yf
from datetime import datetime, timedelta
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

def calc_change_percentage(df_indices):
    """
    Calculate the change in percentage and absolute value for stock indices.
    Args:
        df_indices (DataFrame): DataFrame containing stock indices data.
    Returns:
        DataFrame: DataFrame with additional columns for change in percentage and absolute value.
    """
    change = df_indices['Close'].diff().iloc[-1]
    last_date = df_indices.index[-1]
    indices_list = ['^DJI', '^SPX', '^IXIC', '^SOX']

    change_percentage = df_indices['Close'].pct_change().iloc[-1] * 100
    for idx in indices_list:
        df_indices.loc[last_date, ('Change$', idx)]  = np.round(change[idx], 2)
        df_indices.loc[last_date, ('Change%', idx)]  = f"{np.round(change_percentage[idx], 2)}%"

    df_indices['Close'] = np.round(df_indices['Close'],    2)
    return df_indices

def get_close_price(tickers, day):
    """
    Fetch the close price of given tickers for the last 'day' days.
    
    Args:
        tickers (list): List of stock tickers.
        day (int): Number of days to look back.
    Returns:
        DataFrame: Close prices of the tickers.
    """
    end_date = datetime.now()
    start_date = end_date - timedelta(days=day)
    stock = yf.Tickers(tickers)
    df = stock.history(start=start_date, end=end_date)
    return df

def print_position_close_price():
    """
    Print the close price of stocks in the user's position.
    """
    ticker_list = os.getenv('TICKER_LIST')
    tickers = ticker_list.split(',')
    df_tickers = get_close_price(tickers, 5)
    print(np.round(df_tickers['Close'].iloc[-1], 2))

def print_indices_close_price():
    """
    Print the close price and change percentage of major indices.
    """
    indices = ['^DJI', '^SPX', '^IXIC', '^SOX']
    selected_columns = [
        ('Close', '^DJI'),
        ('Change%', '^DJI'),
        ('Close', '^SPX'),
        ('Change%', '^SPX'),
        ('Close', '^IXIC'),
        ('Change%', '^IXIC'),
        ('Close', '^SOX'),
        ('Change%', '^SOX'),
    ]
    df_indices = get_close_price(indices, 5)
    df_indices = calc_change_percentage(df_indices)
    last_row = df_indices[selected_columns].iloc[-1]
    for idx in indices:
        close = last_row[('Close', idx)]
        change = last_row[('Change%', idx)]
        print(f"{idx:<7} {close:>10.2f} {change:>8}")

def main():
    """
    Main function to execute the script.
    """
    print_position_close_price()
    print_indices_close_price()


if __name__ == '__main__':
    main()