from models.Portfolio import Portfolio
from models.Asset import Asset
from models.MonteCarlo import MonteCarlo
from typing import Optional
import yfinance as yf
import matplotlib.pyplot as plt
import math
import pandas as pd
import numpy as np
import os


class Viewer:
    """
    A Class which saves and/or prints visualisations.

    Parameters
    ----------
    portfolio: models.Portfolio
        An object which stores information and can calulate
        information on the portfolio.
    
    Attributes
    ----------
    portfolio: models.Portfolio
        Saved from the constructor
    """
    def __init__(self, portfolio: Portfolio):
        self.portfolio = portfolio

    def create_individual_asset_graphs(
            self,
            name: str,
            assets: list[str],
            date1: str,
            date2: Optional[str]=None,
    ) -> None:
        """
        Creates graphs of individual assets on a grid from Date1 until
        Date2. Plots are saved to the "graphs" folder.

        Parameters
        ----------
        name: str
            Name of the file to be saved (excluding extension.)
        assets: list[str]
            A list of tickers.
        date1: str
            Starting date for the visualisations.
        date2: Optional[str]
            Ending date for the visualisations.
            ("None" gives most recent)
        
        Returns
        -------
        None

        Notes
        -----
        Saves to location graphs/{name}.png, prints to terminal.
        Creates folder graphs if it doesn't exist already.
        """
        marketData = yf.download(assets, start=date1, end=date2, progress=False, auto_adjust=False)
        marketData = marketData["Close"]
        
        n_assets = len(assets)
        # Determine grid size (rows and columns) to make it as "square" as possible
        cols = math.ceil(math.sqrt(n_assets))
        rows = math.ceil(n_assets / cols)
        fig, axes = plt.subplots(rows, cols, figsize=(5 * cols, 4 * rows))
        # Makes sure I only need to use one loop.
        axes = np.atleast_1d(axes).flatten()

        for i, asset in enumerate(assets):
            ax = axes[i]
            marketData[asset].plot(ax=ax)
            ax.set_title(f"{asset} Closing Prices")
            ax.set_xlabel("Date")
            ax.set_ylabel("Price")
            ax.grid(True)

        # Removes unused subplots
        for j in range(n_assets, len(axes)):
            fig.delaxes(axes[j])

        plt.tight_layout(h_pad=1, w_pad=1)
        save_path = os.path.join("graphs", f"{name}.png")
        os.makedirs(os.path.dirname(save_path), exist_ok=True)
        fig.savefig(save_path)
        plt.close(fig)
        print(f"Individual graphs written to graphs/{name}.png")
 
    def create_portfolio_graph(
            self,
            restrictions: Optional[dict[str, str]],
            name: str,
            date1: str,
            date2: Optional[str]=None,
    ) -> None:
        """
        Creates a graph of the NAV of the portfolio. Assumes
        continuous rebalancing (weights stay the same). 
        Saves the plot to the "graphs" folder

        Parameters
        ----------
        restrictions: Optional[dict[str, str]]
            To filter the portfolio by. e.g. asset class and/or sector.
        name: str
            Name for the to be saved file (excluding extension).
        date1: str
            starting date for the data.
        date2: str
            ending date for the data. ("None" gives most recent).
        
        Returns
        -------
        None

        Notes
        -----
        Saves a file to graphs/{name}.png, prints to terminal.
        Creates folder graphs if it doesn't exist already.
        """
        portfolio_p = self.portfolio.get_portfolio_prices(restrictions, date1, date2)
        plt.figure(figsize=(10,5))
        plt.plot(
            portfolio_p.index,
            portfolio_p["Portfolio Price"],
            label="Portfolio NAV",
            linewidth=2,
        )
        if restrictions is None:
            title = ""
        else:
            title = f"{restrictions.get('asset_class', '')} {restrictions.get('sector', '')}"
        plt.title(f"{title} Portfolio Performance", fontsize=12)
        plt.xlabel("Date")
        plt.ylabel("Price")
        plt.grid(True, alpha=0.3)
        plt.legend()
        plt.tight_layout()
        save_path = os.path.join("graphs", f"{name}.png")
        os.makedirs(os.path.dirname(save_path), exist_ok=True)
        plt.savefig(save_path)
        print(f"Portfolio NAV graph written to graphs/{name}.png")
    
    def create_monte_carlo_graph(
            self,
            restrictions: Optional[dict[str, str]],
            name: str,
            startDate: str,
            endDate: Optional[str]=None,
            n: int=100000,
            months: int=12*15,
    ) -> None:
        """
        Creates a graph including historical data and Monte Carlo
        Simulations (20 realizations + quantiles) and saves them to
        the graphs folder.

        Parameters
        ----------
        restrictions: Optional[dict[str, str]]
            To filter the portfolio by. e.g. asset class and/or sector.
        name: str
            Name of the file to be saved. (excluding extension)
        startDate: str
            starting date for the historical data.
        endDate: str
            ending date for the historical data
            ("None" gives most recent). Also the starting point for
            the Monte Carlo simulations
        n: int
            Number of simulations (max 100000 min 1)
        months: int
            Number of months per simulation.
        
        Returns
        -------
        None

        Notes
        -----
        Saves a file to graphs/{name}.png, prints to terminal.
        Creates folder graphs if it doesn't exist already.
        """
        montecarlo = MonteCarlo(self.portfolio)
        history, sims, future_index = montecarlo.simulate_paths(restrictions, startDate, endDate, n=n, months=months)

        plt.figure(figsize=(10, 5))

        plt.plot(history.index, history["Portfolio Price"], label="Historical NAV", color="black", linewidth=2)

        # Quantiles
        q05 = np.percentile(sims, 5, axis=1)
        q25 = np.percentile(sims, 25, axis=1)
        q50 = np.percentile(sims, 50, axis=1)
        q75 = np.percentile(sims, 75, axis=1)
        q95 = np.percentile(sims, 95, axis=1)

        # Fill percentile bands
        plt.fill_between(future_index, q05, q95, color="blue", alpha=0.1, label="5–95% range")
        plt.fill_between(future_index, q25, q75, color="blue", alpha=0.2, label="25–75% range")

        # Median path
        plt.plot(future_index, q50, color="blue", linewidth=2, label="Median path")

        # A few sample paths
        plt.plot(future_index, sims[:, :20], color="blue", alpha=0.2, linewidth=1)

        if restrictions is None:
            title = ""
        else:
            title = f"{restrictions.get('asset_class', '')} {restrictions.get('sector', '')}"

        plt.title(f"{title} Monte Carlo Portfolio Simulation", fontsize=12)
        plt.xlabel("Date")
        plt.ylabel("Portfolio Price")
        plt.grid(True, alpha=0.3)
        plt.legend()
        plt.tight_layout()

        save_path = os.path.join("graphs", f"{name}.png")
        os.makedirs(os.path.dirname(save_path), exist_ok=True)
        plt.savefig(save_path)
        plt.close()
        print(f"Monte Carlo graph written to graphs/{name}.png")

    def display_summary(self) -> None:
        """
        Prints the portfolio to the terminal as a table.

        Parameters
        ----------
        None

        Returns
        -------
        None

        Notes
        -----
        Prints to the terminal.
        """
        assets = self.portfolio.assets.values()
        df = pd.DataFrame(
            {
                "Ticker": [asset.ticker for asset in assets],
                "Asset Name": [asset.name for asset in assets],
                "Sector": [asset.sector for asset in assets],
                "Asset Class": [asset.asset_class for asset in assets],
                "Quantity": [
                    asset.quantity[0]
                    if len(asset.quantity) == 1 else asset.quantity
                    for asset in assets
                ],
                "Purchase Price": [
                    asset.purchase_price[0]
                    if len(asset.purchase_price) == 1 else asset.purchase_price
                    for asset in assets],
                "Transaction Value": [
                    asset.transaction_values[0]
                    if len(asset.transaction_values) == 1
                    else asset.transaction_values for asset in assets
                ],
                "Current Value": [asset.current_value for asset in assets],
            },
        )
        print()
        print(df.to_markdown(index=False, tablefmt="pipe"))
    
    def display_weights(self, restrictions: Optional[dict[str, str]]=None) -> None:
        """
        Prints the weight of the filtered portfolio w.r.t. total
        portfolio and prints weights of the filtered portfolio to
        the terminal in a table.

        Parameters
        ----------
        restrictions: Optional[dict[str, str]]
            To filter the portfolio by e.g. asset class and/or sector.
        
        Returns
        -------
        None

        Notes
        -----
        prints to the terminal.
        """
        weights, class_sector_value, total = self.portfolio.get_portfolio_weights(restrictions)
        tickers = []
        weight_p_asset = []
        for ticker, weight in weights.items():
            tickers.append(ticker)
            weight_p_asset.append(round(weight, 3))

        if restrictions is None:
            print("\nPortfolio Weights (Total):")
        else:
            # I need to use single quotes in the 'get' methods because of the f string.
            print(
                f"\nWeight {restrictions.get('asset_class', '')} {restrictions.get('sector','')}"
                f" w.r.t. total portfolio: {round(class_sector_value/total, 3)}\n"
            )
            print(
                f"\n{restrictions.get('asset_class', '')} {restrictions.get('sector','')} "
                f"portfolio weights"
            )
        
        df = pd.DataFrame({"Ticker": tickers, "Weights": weight_p_asset})
        print(df.to_markdown(index=False, tablefmt="pipe"))
