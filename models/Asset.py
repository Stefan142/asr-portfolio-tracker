import yfinance as yf


class Asset:
    """
    A class for an asset. Used to store data and
    characteristics of a particular asset.

    Parameters
    ----------
    ticker: str
        Ticker of the asset.
    sector: str
        Sector of the asset.
    asset Class: str
        Asset Class of the asset.
    quantity int:
        The quantity of the asset to hold.
    purchase_price int:
        The purchase price of the asset.

    Attributes:
    -----------
    ticker: str
        Stored from the constructor.
    name: str
        Full name of the asset retrieved from yahoo finance API.
    sector: str
        Stored from the constructor.
    asset_class: str
        Stored from the constructor.
    quantity: list[int]
        Transformed the quantity from the constructor to a list.
    purchase_price: list[int]
        Transformed the purchase price from the constructor to a list.
    """
    def __init__(
            self,
            ticker: str,
            sector: str,
            asset_class: str,
            quantity: int,
            purchase_price: float,
    ):
        self.ticker = ticker
        self.name = yf.Ticker(self.ticker).info.get(
            "longName",
            f"No long name found for {self.ticker}",
        )
        self.sector = sector
        self.asset_class = asset_class
        self.quantity = [quantity]
        self.purchase_price = [purchase_price]
        # This suffices. We use daily data, so constant updating not required.
        self.current_value = self.calculate_current_value()
        self.transaction_values = self.calculate_transaction_values()

    def buy(self, quantity: int, price: float) -> None:
        """
        Add a quantity and purchase price to the asset.
        This allows for buying more of the same asset 
        by the user.

        Parameters
        ----------
        quantity: int
            Quantity to add to the asset.
        price: float
            Purchase price to add to the asset.
        
        Returns
        -------
        None

        Notes
        -----
        Asjusts self.quantity and self.purchase_price.
        """
        self.quantity.append(quantity)
        self.purchase_price.append(price)

    def last_price(self) -> float:
        """
        Retrieves the latest price of the asset known
        from the Yahoo finance API. (20 minute delay allegedly).

        Parameters
        ----------
        None

        Returns
        -------
        float
            The latest price of the Asset.
        
        Notes
        -----
        Prints to the terminal if the ticker does not exist.
        """
        return yf.Ticker(self.ticker).fast_info.get("lastPrice", "No Last Price Found")

    def calculate_transaction_values(self) -> list[float]:
        """
        Total cost of the transaction: quantity * purchase_price
        
        Parameters
        ----------
        None

        Returns
        -------
        list[float]
            A list of all the transaction costs for the asset.
        """
        return [quantity*price for quantity, price in zip(self.quantity, self.purchase_price)]

    def calculate_current_value(self) -> float:
        """
        Calculates the current value of the allocation in the asset.
        
        Parameters
        ----------
        None

        Returns
        -------
        float
            The total current value of the allocation in the asset.
        """
        return sum(self.quantity) * self.last_price()
