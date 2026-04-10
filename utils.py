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
        'INDEX_LIST': os.getenv('INDEX_LIST', '^DJI'),
        'FETCH_DAYS': int(os.getenv('DAYS', 60)),
    }

def make_pretty_date(date_str: str) -> str:
    """
    Convert a date string from YYYY-MM-DD format to a more human-readable format.
    Args:
        date_str (str): The date string in YYYY-MM-DD format.
    Returns:
        str: The date string in a more human-readable format.
    """
    date_obj = datetime.strptime(date_str, '%Y-%m-%d')
    pretty_date = date_obj.strftime('%B %d, %Y')
    return pretty_date

def color_text(text: str, number: float) -> str:
    """
    Color the text based on the number's value.
    Args:
        text (str): The text to color.
        number (float): The number to evaluate.
    Returns:
        str: The colored text.
    """
    if number > 0:
        return f"\033[92m{text:>10}\033[0m"  # Green
    elif number < 0:
        return f"\033[91m{text:>10}\033[0m"  # Red
    else:
        return f"{text:>10}"

def get_requested_date(arg_req_date, fetch_days):
    """
    Validate and convert the requested date string to a datetime object.
    Args:
        arg_req_date (str): The requested date in YYYY-MM-DD format.
        fetch_days (int): Number of days to look back for fetching data.
    Returns:
        datetime: The validated requested date as a datetime object.
    """
    req_date = datetime.strptime(arg_req_date, "%Y-%m-%d")
    now = datetime.now()
    start = now - timedelta(days=fetch_days)
    if req_date < start or req_date > now:
        print(f"Request date {req_date} is out of range.")
        sys.exit()
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
    df = stock.history(start=start_date, end=end_date, progress=False)
    return df