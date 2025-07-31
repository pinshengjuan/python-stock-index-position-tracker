import os
from utils import load_config, get_requested_date, get_close_price

def calc_change_percentage(df_indices):
    """
    Calculate the percentage change for major stock indices.
    Args:
        df_indices (DataFrame): DataFrame containing close prices of indices.
    Returns:
        DataFrame: DataFrame with additional columns for percentage change.
    """
    indices_list = ['^DJI', '^SPX', '^IXIC', '^SOX']

    change_percentage = (df_indices['Close'].pct_change() * 100).round(2).astype(str) + '%'
    for idx in indices_list:
        df_indices.loc[df_indices.index, ('Change%', idx)] = change_percentage.loc[df_indices.index, idx]
    return df_indices

def print_position_close_price(req_date, fetch_days):
    """
    Print the close price of the user's stock positions.
    Args:
        req_date (int): Requested date for fetching data.
        fetch_days (int): Number of days to look back for fetching data.
    Returns:
        None
    """
    ticker_list = os.getenv('TICKER_LIST')
    tickers = ticker_list.split(',')
    df_tickers = get_close_price(tickers, fetch_days)
    if req_date == -1:
        req_date = str(df_tickers.index[-1].date())
    print(df_tickers.loc[req_date, ('Close', tickers)].round(2))

def print_indices_close_price(req_date, fetch_days):
    """
    Print the close price and change percentage of major stock indices.
    Args:
        req_date (int): Requested date for fetching data.
        fetch_days (int): Number of days to look back for fetching data.
    Returns:
        None
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
    df_indices = get_close_price(indices, fetch_days)
    if req_date == -1:
        req_date = str(df_indices.index[-1].date())
    df_indices = calc_change_percentage(df_indices)
    req_row = df_indices.loc[req_date, selected_columns].round(2)
    for idx in indices:
        close = req_row[('Close', idx)]
        change = req_row[('Change%', idx)]
        print(f"{idx:<7} {close:>10.2f} {change:>8}")

def main():
    """
    Main function to execute the script.
    """
    config = load_config()
    fetch_days = config['FETCH_DAYS']
    req_date = get_requested_date(fetch_days)

    print_position_close_price(req_date, fetch_days)
    print_indices_close_price(req_date, fetch_days)


if __name__ == '__main__':
    main()