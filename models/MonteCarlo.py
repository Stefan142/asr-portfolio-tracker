from models.Portfolio import Portfolio
from typing import Optional, Tuple
import yfinance as yf
import numpy as np
import pandas as pd

class MonteCarlo:
    """
    Performs the Monte Carlo simulation.

    Parameters
    ----------
    portfolio: models.Portfolio
        A class which stores the portfolio state and information.
    
    Attributes
    ----------
    portfolio: models.Portfolio
        Stored from the constructor.
    """
    def __init__(self, portfolio: Portfolio):
        self.portfolio = portfolio

    def simulate_paths(
            self,
            restrictions: Optional[dict[str, str]],
            startDate: str,
            endDate: str,
            n: int=100000,
            months: int=12*15,
    ) -> Tuple[pd.DataFrame, np._typing.NDArray[np.float64], pd.DatetimeIndex]:
        """
        Simulates the paths of a Monte Carlo simulation.

        Parameters
        ----------
        restrictions: Optional[dict[str,str]]
            A dictionary containing wheter the simulation should be
            done for a particular asset class and/or sector.
        startDate: str
            Starting date for historical data.
        endDate:
            Ending date for historical data, and starting point
            for the Monte Carlo simulation.
        n: int
            Number of simulations to perform.
        months: int
            The number of months to perform each simulation for.
        
        Returns
        -------
        Tuple[pd.DataFrame, np.typing.NDArray[np.float64], pd.DatetimeIndex]
            A tuple containing the historical data between startDate
            and endDate, The monte Carlo simulations (months*n matrix),
            The dates for the monte carlo simulations. (Not done in 
            pandas df to save memory.)
        """
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
