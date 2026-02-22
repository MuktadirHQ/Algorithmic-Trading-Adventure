import yfinance as yf
import pandas as pd
from datetime import datetime

class AlgorithmicTrading:
    def __init__(self, symbol, start_date, end_date, budget=5000.0):
        self.symbol = symbol
        self.start_date = start_date
        self.end_date = end_date
        self.budget = budget
        self.data = None
        self.position = 0
        self.cash = budget
        self.trade_log = []

    def fetch_data(self):
        df = yf.download(self.symbol, start=self.start_date, end=self.end_date)
        df = pd.DataFrame(df)
        if isinstance(df.columns, pd.MultiIndex):
            df.columns = df.columns.get_level_values(0)
        df.ffill(inplace=True)
        df.drop_duplicates(inplace=True)
        self.data = df

    def compute_moving_averages(self):
        close_prices = self.data["Close"]
        self.data["SMA_50"] = close_prices.rolling(window=50).mean()
        self.data["SMA_200"] = close_prices.rolling(window=200).mean()
        self.data["Safe_Close"] = close_prices.ffill()

    def run_strategy(self):
        self.compute_moving_averages()
        for i in range(1, len(self.data)):
            row_prev = self.data.iloc[i - 1]
            row = self.data.iloc[i]

            # golden cross: SMA_50 crosses above SMA_200
            if (
                self.position == 0
                and row_prev["SMA_50"].item() < row_prev["SMA_200"].item()
                and row["SMA_50"].item() >= row["SMA_200"].item()
            ):
                price = float(row["Safe_Close"])
                qty = int(self.cash // price)
                if qty > 0:
                    self.position = qty
                    self.cash -= qty * price
                    self.trade_log.append(("BUY", row.name, price, qty))

            # death cross: SMA_50 crosses below SMA_200
            elif (
                self.position > 0
                and row_prev["SMA_50"].item() > row_prev["SMA_200"].item()
                and row["SMA_50"].item() <= row["SMA_200"].item()
            ):
                price = float(row["Safe_Close"])
                qty = self.position
                self.position = 0
                self.cash += qty * price
                self.trade_log.append(("SELL", row.name, price, qty))

        # force close last bar if still in position
        if self.position > 0:
            last_row = self.data.iloc[-1]
            price = float(last_row["Safe_Close"])
            qty = self.position
            self.position = 0
            self.cash += qty * price
            self.trade_log.append(("SELL_FINAL", last_row.name, price, qty))

    def results(self):
        pnl = self.cash - self.budget
        trades_df = pd.DataFrame(self.trade_log, columns=["Side", "Date", "Price", "Qty"])

        filename = f"trade_results_{datetime.now().strftime('%Y%m%d_%H%M%S')}.txt"
        with open(filename, "w", encoding="utf-8") as f:
            f.write(f"Symbol: {self.symbol}\n")
            f.write(f"PnL: {pnl}\n")
            f.write("Trades:\n")
            f.write(trades_df.to_string(index=False))

        return pnl, trades_df


if __name__ == "__main__":
    
    # symbol = input("Enter the stock symbol (e.g., 'USD'): ")
    symbol = input("Enter the stock symbol (e.g., 'AAPL' or 'MSFT' or 'USD'): ").strip().upper() or "AAPL"
    start_date = input("Enter the start date (YYYY-MM-DD): ")
    end_date = input("Enter the end date (YYYY-MM-DD): ")
    
    bot = AlgorithmicTrading(symbol, start_date, end_date)
    bot.fetch_data()
    bot.run_strategy()
    pnl, trades = bot.results()
    
    print(trades.head())
    print("PnL:", round(pnl, 2))