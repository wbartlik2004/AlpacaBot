import alpaca_trade_api as tradeapi
from datetime import datetime, timedelta
import yfinance as yf
import time
from talipp.indicators import SMA


def buy():
    api.submit_order(
        symbol=symbol,
        qty=qty,
        side='buy',
        type='market',
        time_in_force='gtc'  # Good 'til canceled
    )


def sell():
    api.submit_order(
        symbol=symbol,
        qty=qty,
        side='sell',
        type='market',
        time_in_force='gtc'  # Good 'til canceled
    )


def get_stock_data(symboly, start_datey, end_datey, intervaly='1m'):
    # Download historical data as a Pandas DataFrame
    data = yf.download(symboly, start=start_datey, end=end_datey, interval=intervaly)
    return data


def get_stock_price(symbol_used):
    stock = yf.Ticker(symbol_used)
    prices = stock.history(period="1d")["Close"].iloc[-1]
    return prices


forever = 1

while forever == 1:
    APCA_API_BASE_URL = 'https://paper-api.alpaca.markets'
    APCA_API_KEY_ID = 'PK3QO6SX4MCNV0TL3OGV'
    APCA_API_SECRET_KEY = 'XkN8QY7V99yHBYb07PbkpXGOGT33xQbYtC8bhOvQ'
    api = tradeapi.REST(APCA_API_KEY_ID, APCA_API_SECRET_KEY, base_url=APCA_API_BASE_URL, api_version='v2')
    end_date = int(time.time())  # Unix timestamp representing the current time
    start_date = int((datetime.fromtimestamp(end_date) - timedelta(days=5)).timestamp())
    positions = api.list_positions()

    symbol = 'SPY'  # Replace with the desired stock symbol
    qty = 20  # Replace with the desired quantity of shares
    window_size = 50
    mode = 2  # 0 means we are looking to sell, 1 means we have a positions and we are looking to sell

    if len(positions) > 0:
        print("You currently have open positions.")
        for position in positions:
            print(f"Symbol: {position.symbol}, Quantity: {position.qty}, Side: {position.side},"
                  f" Average Entry Price: {position.avg_entry_price}")
        mode = 1  # looking to sell
    else:
        print("You currently do not have any open positions.")
        mode = 0  # looking to buy

    while mode == 0:
        end_date = int(time.time())  # Unix timestamp representing the current time
        start_date = int((datetime.fromtimestamp(end_date) - timedelta(days=5)).timestamp())
        stock_data = get_stock_data(symbol, start_date, end_date)
        sma = SMA(period=window_size, input_values=stock_data['Close'].tolist())
        try:
            price = get_stock_price(symbol)
            times = datetime.now()

            print(f"Current price of {symbol} is: {price:.3f} at {times} and SMA = {sma[-1]:.3f}")
            if (price > sma[-1]) and (sma[-2] < sma[-1]) and \
                    (sma[-3] < sma[-2]):
                buy()
                mode = 1
                print(f"Buy signal: Current price {price:.3f} > moving average {sma[-1]:.3f} "
                      f"Current Price of {symbol}:")
                while mode == 1:
                    end_date = int(time.time())  # Unix timestamp representing the current time
                    start_date = int((datetime.fromtimestamp(end_date) - timedelta(days=5)).timestamp())
                    stock_data = get_stock_data(symbol, start_date, end_date)
                    sma = SMA(period=window_size, input_values=stock_data['Close'].tolist())
                    try:
                        price = get_stock_price(symbol)
                        times = datetime.now()
                        print(f"Current price of {symbol} is: {price:.3f} at {times} and SMA = "
                              f"{sma[-1]:.3f}")
                        if price < sma[-1]:
                            sell()
                            mode = 2
                            print(
                                f"sell signal:Current pr {price:.3f} < moving average {sma[-1]:.3f} "
                                f"Current Price of {symbol}:")
                    except Exception as e:
                        print(f"Error fetching stock price: {e}")
                    time.sleep(10)
        except Exception as e:
            print(f"Error fetching stock price: {e}")
        time.sleep(10)
