from models.Portfolio import Portfolio
from models.Asset import Asset
from views.create_views import Viewer
import yfinance as yf
from datetime import datetime as dt
import sys

class Controller:
    def __init__(self):
        self.portfolio = Portfolio()
        self.viewer = Viewer(self.portfolio)
        self.asset_classes = {
            "Equities",
            "Fixed Income",
            "Cash & Cash Equivalents",
            "Commodities",
            "Real Estate",
            "Derivatives",
            "Private Equity",
            "Hedge Funds",
            "Digital Assets",
            "Other",
            "All",
        }
        self.sectors = {
            "Energy",
            "Materials",
            "Industrials",
            "Consumer Discretionary",
            "Consumer Staples",
            "Health Care",
            "Financials",
            "Information Technology",
            "Communication Services",
            "Utilities",
            "Real Estate",
            "Other",
            "All",
        }
    
    def handle_command(self, command):
        command = command.strip().upper()
        if command.strip().upper() == "ADD":
            self.add_to_portfolio()
        
        elif command.strip().upper() == "SHOW":
            self.show_table()

        elif command.strip().upper() == "GRAPH":
            self.show_graph()
        
        elif command.strip().upper() == "DELETE":
            self.delete_from_portfolio()
        
        else:
            print("\nUnrecognized command\n")
    
    def delete_from_portfolio(self):
        ticker = input("Ticker to delete: ")
        self.portfolio.delete_asset(ticker)

    def add_to_portfolio(self):
        while True:
            try:
                ticker = input("Ticker: ")
                # I need some way to check if ticker exists
                int(yf.Ticker(ticker).fast_info["lastPrice"])
                break
            except KeyboardInterrupt:
                print("\n\nGoodbye!\n")
                sys.exit(0)
            except:
                print(f"\n{ticker} does not exist in yahoo finance API\n")
        
        while True:
            try:
                asset_class = input("Asset Class: ").strip().title()
                if asset_class not in self.asset_classes:
                    raise ValueError
                break
            except KeyboardInterrupt:
                print("\n\nGoodbye!\n")
                sys.exit(0)
            except:
                print(f"\nInvalid Asset Class, choose one of {self.asset_classes}\n")

        while True:
            try:
                sector = input("Sector: ").strip().title()
                if sector not in self.sectors:
                    raise ValueError
                break
            except KeyboardInterrupt:
                print("\n\nGoodbye!\n")
                sys.exit(0)
            except:
                print(f"\n invalid {sector}, choose one of {self.sectors}\n")

        while True:
            try:
                quantity = int(input("Quantity: ").strip())
                break
            except KeyboardInterrupt:
                print("\n\nGoodbye!\n")
                sys.exit(0)
            except:
                print(f"\n{quantity} is not numeric, please provide numeric value.\n")

        while True:
            try:
                purchase_price = float(input("Purchase Price: ").strip())
                break
            except KeyboardInterrupt:
                print("\n\nGoodbye!\n")
                sys.exit(0)
            except:
                print(f"\n{purchase_price} is not numeric, please provide numeric value.\n")     
        
        if self.portfolio.check_if_present(ticker):
            self.portfolio[ticker].buy_or_sell(quantity, purchase_price)
        else:
            self.portfolio.add_new_asset(Asset(ticker, sector, asset_class, quantity, purchase_price))
        print(f"\nSuccesfully added {quantity} of {ticker} to the portfolio.\n")
        
    
    def show_table(self):
        table_type = input("Table (Summary or Weights): ").strip().capitalize()
        if table_type == "Summary":
            self.viewer.display_summary()
        elif table_type == "Weights":
            restrictions = self.retrieve_restrictions()
            self.viewer.display_weights(restrictions=restrictions)
        else:
            print("\nInvalid Table type, choose one of the available options.\n")

    def retrieve_restrictions(self):
        while True:
            try:
                asset_class = input("By Asset Class (all or specific asset class): ").strip().title()
                if asset_class not in self.asset_classes:
                    raise ValueError
                break
            except KeyboardInterrupt:
                print("\n\nGoodbye!\n")
                sys.exit(0)
            except:
                print(f"\nInvalid Asset Class, choose one of {self.asset_classes}\n")

        while True:
            try:
                sector = input("By Sector (all or specific sector): ").strip().title()
                if sector not in self.sectors:
                    raise ValueError
                break
            except KeyboardInterrupt:
                print("\n\nGoodbye!\n")
                sys.exit(0)
            except:
                print(f"\n invalid {sector}, choose one of {self.sectors}\n")
        restrictions = {}
        if asset_class != "All":
            restrictions["asset_class"] = asset_class
        if sector != "All":
            restrictions["sector"] = sector
        if len(restrictions) == 0:
            restrictions = None
        return restrictions

    
    def show_graph(self):
        graph_type = input("Type (Individual Assets/Portfolio/Monte Carlo): ").strip().title()
        while True:
            try:
                date1 = input("Start date for the graph (YYYY-MM-DD): ").strip()
                dt.strptime(date1, "%Y-%m-%d")
                date2 = input("End date for the graph (YYYY-MM-DD or None): ").strip().capitalize()
                if date2.strip().capitalize() != "None":
                    dt.strptime(date2, "%Y-%m-%d")
                else:
                    date2 = None
                break
            except KeyboardInterrupt:
                print("\n\nGoodbye!\n")
                sys.exit(0)
            except:
                print("\nInvalid date entered, please provide valid format: YYYY-MM-DD\n")
        name_graph = input("Provide a name for the graph (no extension): ")
        if graph_type == "Individual Assets":
            while True:
                try:
                    assets = input("Asset tickers (Chain with ,): ").replace(" ", "").strip().split(",")
                    if not isinstance(assets, list):
                        assets = [assets]
                    for asset in assets:
                        int(yf.Ticker(asset).fast_info["lastPrice"])
                    break
                except KeyboardInterrupt:
                    print("\n\nGoodbye!\n")
                    sys.exit(0)
                except:
                    print(f"\n{asset} not present in yahoo finance API.\n")
            self.viewer.create_individual_asset_graphs(name_graph, assets, date1, date2=date2)
        
        elif graph_type == "Portfolio":
            restrictions = self.retrieve_restrictions()
            self.viewer.create_portfolio_graph(restrictions, name_graph, date1, date2=date2)
        
        elif graph_type == "Monte Carlo":
            restrictions = self.retrieve_restrictions()
            while True:
                try:
                    sims = int(input("Number of simulations: ").strip())
                    if 0 > sims > 100000:
                        print("\nMaximum allowed is 100000 and a Minimum of 1\n")
                    else:
                        break
                except KeyboardInterrupt:
                    print("\n\nGoodbye!\n")
                    sys.exit(0)
                except:
                    print("\nProvide an integer.\n")

            while True:
                try:
                    years = float(input("Number of years (min 1/12, max 100): ").strip())
                    if years*12 % 1 != 0:
                        print("\nUnable to process, make sure input * 12 is a positive integer.\n")
                    elif years > 100:
                        print("\ninput exceeded 100, make sure input is below 100\n")
                    else:
                        break
                except KeyboardInterrupt:
                    print("\n\nGoodbye!\n")
                    sys.exit(0)
                except:
                    print("\nProvide an integer.\n")
            
            self.viewer.create_monte_carlo_graph(restrictions, name_graph, date1, date2, n=sims, months=int(12*years))
