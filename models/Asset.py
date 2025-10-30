import yfinance as yf


class Asset:
    def __init__(self, ticker, sector, asset_class, quantity, purchase_price):
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

    def buy_or_sell(self, quantity, price) -> None:
        self.quantity.append(quantity)
        self.purchase_price.append(price)

    def last_price(self) -> float:
        return yf.Ticker(self.ticker).fast_info.get("lastPrice", "No Last Price Found")

    def calculate_transaction_values(self) -> list[float]:
        """Total cost when bought"""
        return [quantity*price for quantity, price in zip(self.quantity, self.purchase_price)]

    def calculate_current_value(self) -> float:
        """Most recent market value"""
        return sum(self.quantity) * self.last_price()

    def gain_loss(self) -> float:
        last_price = self.last_price()
        return sum(
            [
                last_price*quantity - transaction
                for transaction, quantity in zip(self.transaction_values, self.quantity)
            ],
        )
