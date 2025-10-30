from models.Asset import Asset
from typing import Optional, Tuple
import pandas as pd
import yfinance as yf


class Portfolio:
    """
    A class for a portfolio, Stores assets and performs calculations.

    Parameters
    ----------
    None

    Attributes
    ----------
    assets: dict[str, Asset]
        Storage for the assets.
    """
    def __init__(self):
        self.assets = {}
    
    def get_portfolio_weights(
            self,
            restrictions: Optional[dict[str, str]],
    ) -> Tuple[dict[str, float], float, float]:
        """
        Retrieves the relative weights of the assets under
        "restrictions"

        Parameters
        ----------
        restrictions: Optional[dict[str, str]]
            Contains the Asset Class and/or the Sector.
            Used to filter the Assets for the weight calculation.
        
        Returns
        -------
        Tuple[dict[str, float], float, float]
            Relative weight of the asset w.r.t. asset class and/or
            sector being the "total",
            total value of the asset class and/or
            sector w.r.t. the total portfolio, Value of the total
            portfolio.
        """
        total_value = sum([asset.current_value for ticker, asset in self.assets.items()])
        considered_assets = {}
        
        if restrictions == None:
            total_relative_value = sum(
                [asset.current_value for ticker, asset in self.assets.items()],
            )
            considered_assets = self.assets
        
        else:
            total_relative_value = 0
            for ticker, asset in self.assets.items():
                # I can do this, because if I have no restriction on the variable, "get" returns
                # the second argument, hence less code, same functionality.
                if (asset.sector == restrictions.get("sector", asset.sector)
                    and asset.asset_class == restrictions.get("asset_class", asset.asset_class)):
                    
                    total_relative_value += asset.current_value
                    considered_assets[ticker] = asset
            
        relative_weights = {}
        for ticker, asset in considered_assets.items():
            relative_weights[ticker] = asset.current_value / total_relative_value
        
        return relative_weights, total_relative_value, total_value

    def add_new_asset(self, asset: Asset) -> None:
        """
        Adds a new asset to the portfolio.

        Parameters
        ----------
        asset: models.Asset
            The asset to add to the portfolio.

        Returns
        -------
        None

        Notes
        -----
        Adjusts self.assets
        """
        self.assets[asset.ticker] = asset
    
    def check_if_present(self, ticker: str) -> bool:
        """
        Checks if a ticker is present in self.assets

        parameters
        ----------
        ticker: str
            The ticker to check for.
        
        Returns
        -------
        bool
            If it is present True, else False.
        """
        return ticker in self.assets

    def get_portfolio_prices(
            self,
            restrictions: Optional[dict[str, str]],
            date1: str,
            date2: Optional[str]=None,
    ) -> pd.DataFrame:
        """
        Get prices of the portfolio (or a subset of it).
        Portfolio is continuously rebalanced. (Weights stay the same)

        Parameters
        ----------
        restrictions: Optional[dict[str, str]]
            To filter the portfolio by asset class and/or sector.
        date1: str
            Starting date for the data.
        date2: Optional[str]
            Ending date for the data. ("None" retrieves most recent.)

        Returns
        -------
        pd.DataFrame
            A dataframe containing the NAV of
            the rebalanced filtered portfolio.
        """
        weights, _, _ = self.get_portfolio_weights(restrictions)
        tickers = list(weights.keys())
        marketData = yf.download(tickers, start=date1, end=date2, progress=False, auto_adjust=False)
        marketData = marketData["Close"][tickers]
        marketData.dropna(inplace=True)
        return marketData.mul(pd.Series(weights)).sum(axis=1).to_frame("Portfolio Price")
    
    def delete_asset(self, ticker: str) -> None:
        """
        Deletes an asset from the portfolio.

        Parameters
        ----------
        ticker: str
            Ticker of the asset.

        Returns
        -------
        None

        Notes
        -----
        Prints to the terminal.
        """
        if ticker in self.assets:
            del self.assets[ticker]
            print("Ticker deleted")
        else:
            print("Ticker not in portfolio, so no deletion.")
