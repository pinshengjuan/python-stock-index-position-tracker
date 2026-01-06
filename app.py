import os
import gc
from utils import load_config, get_requested_date, get_close_price

def calc_change_percentage(df, ticker_list):
    """
    Calculate the percentage change in close prices for the given DataFrame.
    Args:
        df (DataFrame): DataFrame containing close prices of stock tickers.
        ticker_list (list): List of stock ticker symbols.
    Returns:
        DataFrame: DataFrame with an additional column for percentage change.
    """
    close_filled = df['Close'].ffill()
    change_percentage = (close_filled.pct_change() * 100).round(2).astype(str) + '%'
    for idx in ticker_list:
        df.loc[df.index, ('Change%', idx)] = change_percentage.loc[df.index, idx]
    return df

def print_result(tickers, req_date, fetch_days):
    """
    Print the close prices and percentage change for the specified stock tickers.
    Args:
        tickers (list): List of stock ticker symbols.
        req_date (datetime or str): The requested date for fetching data.
        fetch_days (int): Number of days to look back for fetching data.
    Returns:
        None: Prints the results to the console.
    """
    selected_columns = []
    for index in tickers:
        selected_columns.append(('Close', index))
        selected_columns.append(('Change%', index))
    df = get_close_price(tickers, fetch_days)
    df = calc_change_percentage(df, tickers)

    """Format requested date"""
    if req_date == -1:
        req_date = str(df.index[-1].date())
    else:
        req_date = f'{req_date:%Y-%m-%d}'
    
    """Print requested date close price and change%"""
    shown_req_date = "******* [{}] *******".format(req_date)
    try:
        req_row = df.loc[req_date, selected_columns].round(2)
    except KeyError:
        print(shown_req_date)
        print("No data available for the requested date.\n")
        del df
        gc.collect()
        return
    print(shown_req_date)
    req_row = df.loc[req_date, selected_columns].round(2)
    for idx in tickers:
        close = req_row[('Close', idx)]
        change = req_row[('Change%', idx)]
        print(f"{idx:<7} {close:>10.2f} {change:>8}")
    print("\r")
    del df
    gc.collect()

def main():
    """
    Main function to execute the script.
    """
    config = load_config()

    fetch_days = config['FETCH_DAYS']
    tickers = config['TICKER_LIST'].upper().split(',')
    indices = config['INDEX_LIST'].upper().split(',')

    watchlist = [tickers, indices]

    req_date = get_requested_date(fetch_days)

    for idx in watchlist:
        print_result(idx, req_date, fetch_days)

if __name__ == '__main__':
    main()