# python-stock-index-position-tracker

A Python script to track and display the closing prices and daily percentage changes of major stock indices and user-defined stock positions.

## Features

- Fetches recent closing prices for major indices: Dow Jones (^DJI), S&P 500 (^SPX), NASDAQ (^IXIC), and SOX (^SOX)
- Calculates and displays daily percentage and absolute changes for each index
- Prints closing prices for user-specified stock tickers
- Uses [yfinance](https://github.com/ranaroussi/yfinance) for data retrieval
- Loads ticker list from a `.env` file for easy configuration

## Requirements

- Python 3.7+
- `yfinance`
- `numpy`
- `python-dotenv`

Install dependencies with:

```sh
pip install yfinance numpy python-dotenv
```

## Usage

1. Create a `.env` file in the project directory with your stock tickers, e.g.:
    ```
    TICKER_LIST=AAPL,MSFT,GOOGL
    ```

2. Run the script:
    ```sh
    python app.py
    ```

## Output

The script prints the latest closing prices and daily changes for indices and your selected stocks in a readable format:

```
^DJI      44632.99   -0.46%
^SPX       6370.86   -0.30%
^IXIC     21098.29   -0.38%
^SOX       5739.79    0.05%
[Your stock positions' closing prices]
```

## License

MIT License