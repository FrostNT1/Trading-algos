import yfinance as yf
import pandas as pd
from backtesting import Backtest, Strategy
from backtesting.lib import crossover

# Calculate MACD
def calculate_macd(df, short_window=12, long_window=26, signal_window=9):
    df['EMA12'] = df['Close'].ewm(span=short_window, adjust=False).mean()
    df['EMA26'] = df['Close'].ewm(span=long_window, adjust=False).mean()
    df['MACD'] = df['EMA12'] - df['EMA26']
    df['Signal'] = df['MACD'].ewm(span=signal_window, adjust=False).mean()
    return df

# MACD Strategy
class MACD(Strategy):
    def init(self):
        df = self.data.df
        df = calculate_macd(df)
        self.macd = df['MACD'].values
        self.macd_signal = df['Signal'].values

    def next(self):
        if crossover(self.macd, self.macd_signal):
            self.buy()
        elif crossover(self.macd_signal, self.macd):
            self.sell()

# Get historical data using yfinance
data = yf.download('AAPL', start='2018-01-01', end='2020-01-01')

# Add a DataFrame with calculated MACD indicators to the Backtest data
data = calculate_macd(data)

# Backtest
backtest = Backtest(data, MACD, cash=10000, commission=.002, exclusive_orders=True)
print(backtest.run())
