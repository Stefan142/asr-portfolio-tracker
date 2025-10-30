import yfinance as yf
import numpy as np
import pandas as pd


class MonteCarlo:
    def __init__(self, portfolio):
        self.portfolio = portfolio

    def simulate_paths(self, restrictions, startDate, endDate, n=100000, months=12*15):
        portfolio_p = self.portfolio.get_portfolio_prices(restrictions, startDate, endDate)
        portfolio_month_p = portfolio_p.resample('ME').last() 
        log_returns = np.log(portfolio_p / portfolio_p.shift(1)).dropna()

        mu = np.mean(log_returns)
        sigma = np.std(log_returns)
        last_price = portfolio_p.iloc[-1].item()
        last_date = portfolio_p.index[-1]

        random_shocks = np.random.normal(mu, sigma, size=(months, n))
        log_price_paths = np.cumsum(random_shocks, axis=0)
        price_paths = last_price * np.exp(log_price_paths)

        future_index = pd.bdate_range(start=last_date, periods=months + 1, freq="ME")[1:]
        return portfolio_month_p, price_paths, future_index
