import yfinance as yf
import pandas as pd
import matplotlib.pyplot as plt


class Portfolio:
    """
    A simple stock portfolio tracker that allows users to:
    - Add and remove stocks
    - Calculate total portfolio value
    - Plot portfolio performance over time
    """

    def __init__(self):
        self.stocks = {}  # {ticker: quantity}

    def add_stock(self, ticker: str, quantity: int):
        if quantity <= 0:
            raise ValueError("Quantity must be greater than zero.")

        ticker = ticker.upper()
        self.stocks[ticker] = self.stocks.get(ticker, 0) + quantity

    def remove_stock(self, ticker: str, quantity: int):
        ticker = ticker.upper()

        if ticker not in self.stocks:
            print(f"{ticker} not found in portfolio.")
            return

        if quantity <= 0:
            raise ValueError("Quantity must be greater than zero.")

        if quantity >= self.stocks[ticker]:
            del self.stocks[ticker]
        else:
            self.stocks[ticker] -= quantity

    def get_latest_price(self, ticker: str):
        try:
            data = yf.Ticker(ticker).history(period="1d")
            return data["Close"].iloc[-1]
        except Exception:
            print(f"Could not fetch price for {ticker}")
            return 0

    def get_portfolio_value(self) -> float:
        total_value = 0

        for ticker, quantity in self.stocks.items():
            price = self.get_latest_price(ticker)
            total_value += price * quantity

        return total_value

    def plot_portfolio_performance(self, start_date: str, end_date: str):
        portfolio_value = pd.Series(dtype=float)

        for ticker, quantity in self.stocks.items():
            try:
                data = yf.Ticker(ticker).history(
                    start=start_date, end=end_date
                )["Close"]
                portfolio_value = portfolio_value.add(
                    data * quantity, fill_value=0
                )
            except Exception:
                print(f"Skipping {ticker} due to data error.")

        if portfolio_value.empty:
            print("No data to plot.")
            return

        plt.figure(figsize=(10, 5))
        portfolio_value.plot(title="Portfolio Performance Over Time")
        plt.xlabel("Date")
        plt.ylabel("Portfolio Value (USD)")
        plt.grid(True)
        plt.show()

    def portfolio_summary(self):
        print("\nPortfolio Summary")
        print("-" * 30)

        total_value = self.get_portfolio_value()
        print(f"Total Portfolio Value: ${total_value:.2f}\n")

        for ticker, quantity in self.stocks.items():
            price = self.get_latest_price(ticker)
            value = price * quantity
            print(
                f"{ticker}: {quantity} shares | "
                f"Price: ${price:.2f} | "
                f"Value: ${value:.2f}"
            )


if __name__ == "__main__":
    portfolio = Portfolio()

    portfolio.add_stock("AAPL", 10)
    portfolio.add_stock("MSFT", 5)
    portfolio.add_stock("GOOGL", 2)

    portfolio.portfolio_summary()
    portfolio.plot_portfolio_performance(
        start_date="2023-01-01",
        end_date="2024-01-01"
    )
