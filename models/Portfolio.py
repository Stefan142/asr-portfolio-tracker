from models.Asset import Asset
import pandas as pd
import yfinance as yf

class Portfolio:
    def __init__(self):
        self.assets = {}
    
    def get_portfolio_weights(self, restrictions):
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

    def add_new_asset(self, asset: Asset):
        self.assets[asset.ticker] = asset
    
    def check_if_present(self, ticker):
        return ticker in self.assets
    
    def get_portfolio_prices(self, restrictions, date1, date2=None):
        weights, _, _ = self.get_portfolio_weights(restrictions)
        tickers = list(weights.keys())
        marketData = yf.download(tickers, start=date1, end=date2, progress=False, auto_adjust=False)
        marketData = marketData["Close"][tickers]
        marketData.dropna(inplace=True)
        return marketData.mul(pd.Series(weights)).sum(axis=1).to_frame("Portfolio Price")
    
    def delete_asset(self, ticker):
        if ticker in self.assets:
            del self.assets[ticker]
            print("Ticker deleted")
        else:
            print("Ticker not in portfolio, so no deletion.")




# assets_dict = {
#     "AAPL": Asset(ticker="AAPL", sector="Technology", asset_class="Equity", quantity=10, purchase_price=150.0),
#     "MSFT": Asset(ticker="MSFT", sector="Technology", asset_class="Equity", quantity=8,  purchase_price=300.0),
#     "JNJ":  Asset(ticker="JNJ",  sector="Healthcare", asset_class="Equity", quantity=15, purchase_price=160.0),
#     "PG":   Asset(ticker="PG",   sector="Consumer", asset_class="Equity", quantity=20, purchase_price=140.0),
#     "TLT":  Asset(ticker="TLT",  sector="Fixed Income", asset_class="Bond", quantity=5,  purchase_price=130.0),
#     "GLD":  Asset(ticker="GLD",  sector="Commodities", asset_class="Commodity", quantity=12, purchase_price=170.0),
# }

# p = Portfolio(assets_dict)
# restrictions = {"asset_class":"Equity", "sector":"Technology"}
# print(p.get_portfolio_weights(restrictions))