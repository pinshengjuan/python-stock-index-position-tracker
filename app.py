import os
import gc
import argparse
from utils import load_config, color_text, make_pretty_date, get_requested_date, get_close_price

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
    change_percentage = (close_filled.pct_change() * 100).round(2)
    for idx in ticker_list:
        df.loc[df.index, ('Change%', idx)] = change_percentage.loc[df.index, idx]
    return df

def print_result_compact(tickers, req_date, fetch_days):
    selected_columns = []
    for index in tickers:
        selected_columns.append(('Close', index))
    df = get_close_price(tickers, fetch_days)
    df = calc_change_percentage(df, tickers)

    """Format requested date"""
    if req_date == -1:
        req_date = str(df.index[-1].date())
    else:
        req_date = f'{req_date:%Y-%m-%d}'
    
    """Print requested date close price and change%"""
    pretty_date = make_pretty_date(req_date)
    try:
        req_row = df.loc[req_date, selected_columns].round(2)
    except KeyError:
        print(f"No data available for {req_date}")
        del df
        gc.collect()
        return
    print(f'\n{pretty_date}')

    for idx in tickers:
        close = req_row[('Close', idx)]
        print(f'{close:.2f}\n', end='')
    del df
    gc.collect()

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
    pretty_date = make_pretty_date(req_date)
    try:
        req_row = df.loc[req_date, selected_columns].round(2)
    except KeyError:
        print(f"No data available for {req_date}")
        del df
        gc.collect()
        return
    print(f'\n{pretty_date}')
    print('=' * 45)

    # Header
    print(f"{'Ticker':<8} {'Close':>12} {'Change %':>12}")
    print('-' * 45)
    for idx in tickers:
        close = req_row[('Close', idx)]
        change = req_row[('Change%', idx)]
        change_str = f'{change:+.2f}%'
        change_str = color_text(change_str, change)
        print(f'{idx:<8} {close:>12.2f} {change_str}')
    print('=' * 45)
    del df
    gc.collect()

def main():
    """
    Main function to execute the script.
    """
    parser = argparse.ArgumentParser()
    parser.add_argument("-d", "--date", help="Specific date YYYY-MM-DD")
    parser.add_argument("-c", "--compact", action="store_true", help="Compact output")
    args = parser.parse_args()

    config = load_config()

    fetch_days = config['FETCH_DAYS']
    tickers = config['TICKER_LIST'].upper().split(',')
    indices = config['INDEX_LIST'].upper().split(',')

    watchlist = [tickers, indices]

    if args.date:
        req_date = get_requested_date(args.date, fetch_days)
    else:
        req_date = -1 #latest data

    if args.compact:
        print_result_compact(tickers, req_date, fetch_days)
    else:
        for idx in watchlist:
            print_result(idx, req_date, fetch_days)

if __name__ == '__main__':
    main()