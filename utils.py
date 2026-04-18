import sys
import json
import yfinance as yf
from datetime import datetime, timedelta
from typing import Any
from pathlib import Path

def load_config(config_name: str = "config.json") -> dict[str, Any]:
    """
    Load configuration from a JSON file. 
    Falls back to hardcoded defaults if the file is missing or invalid.
    """
    # Define fallback defaults
    default_config = {
        'TICKER_LIST': ['GOOGL'],
        'INDEX_LIST': ['^DJI'],
        'FETCH_DAYS': 60,
    }

    # Use Path for better cross-platform compatibility (macOS/Linux/Windows)
    config_path = Path(__file__).parent / config_name

    if not config_path.exists():
        print(f"Warning: {config_name} not found. Falling back to defaults.")
        return default_config

    try:
        with open(config_path, 'r', encoding='utf-8') as f:
            user_config = json.load(f)
            
            # Merge user config into defaults to ensure all keys exist
            final_config = {**default_config, **user_config}
            
            # print(f"Configuration successfully loaded from: {config_path}")
            return final_config
            
    except json.JSONDecodeError as e:
        print(f"Error: Failed to parse {config_name}. Invalid JSON format: {e}")
        return default_config
    except Exception as e:
        print(f"Unexpected error loading config: {e}")
        return default_config

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