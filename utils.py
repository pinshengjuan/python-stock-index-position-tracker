import os
import sys
import yfinance as yf
from datetime import datetime, timedelta
from typing import Any
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

def load_config() -> dict[str, Any]:
    """
    Load configuration settings from environment variables or defaults.
    Returns:
        dict: Configuration settings.
    """
    return {
        'TICKER_LIST': os.getenv('TICKER_LIST', 'GOOGL'),
        'FETCH_DAYS': int(os.getenv('DAYS', 60)),
    }

def get_requested_date(fetch_days):
    """
    Get the requested date for fetching stock data.
    If a date is provided as a command line argument, validate it.
    If no date is provided, use the latest available data.
    Args:
        fetch_days (int): Number of days to look back for fetching data.
    Returns:
        datetime: The requested date for fetching data.
    Raises:
        SystemExit: If the provided date is invalid or out of range or format is incorrect.
    """
    if len(sys.argv) > 2:
        sys.exit()
    elif len(sys.argv) == 2:
        try:
            datetime.strptime(sys.argv[1], "%Y-%m-%d")
            req_date = datetime.strptime(sys.argv[1], "%Y-%m-%d")
            now = datetime.now()
            start = now - timedelta(days=fetch_days)
            if req_date < start or req_date > now:
                print(f"Request date {req_date} is out of range.")
                sys.exit()
        except ValueError:
            print(f"Invalid argument: {sys.argv[1]}. Please provide an YYYY-mm-dd format for previous days.")
            sys.exit()
    else:
        req_date = -1 #latest data
    return req_date

def get_close_price(tickers, fetch_days):
    """
    Fetch the close prices of the specified stock tickers.
    Args:
        tickers (list): List of stock ticker symbols.
        fetch_days (int): Number of days to look back for fetching data.
    Returns:
        DataFrame: DataFrame containing close prices of the specified tickers.
    """
    end_date = datetime.now()
    start_date = end_date - timedelta(days=fetch_days)
    stock = yf.Tickers(tickers)
    df = stock.history(start=start_date, end=end_date)
    return df