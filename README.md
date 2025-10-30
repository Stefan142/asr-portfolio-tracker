# ASR Portfolio Tracker

## Table of Contents
- [ASR Portfolio Tracker](#asr-portfolio-tracker)
  - [Table of Contents](#table-of-contents)
  - [Requirements and Installation](#requirements-and-installation)
  - [Usage](#usage)
    - [Add](#add)
    - [Delete](#delete)
    - [Show](#show)
    - [Graph](#graph)
  - [Assumptions and Notes](#assumptions-and-notes)

## Requirements and Installation

- This project was tested in a new virtual environment with python version 3.10. Due to type-hinting in the project 3.9+ should suffice.
- Clone this repository.
- run ```pip install -r requirements.txt``` or ```pip install -r requirements.txt``` in the CLI.
- From the root directory of this repository run the following command to start the application: ```python main.py``` or ```python3 main.py```
- Now proceed to the usage section.

## Usage

After running main.py from the root directory, you should see the following in the CLI:

```
a.s.r. Portfolio Tracker
View the README for instructions. C^ (CTRL + C) at any point to quit.
Provide a Command (ADD/DELETE/SHOW/GRAPH): 
```

The tool provides questions to the user, which the user should answer to use the tool. The first one is a command on what general operation should be performed. This is one of these ADD/DELETE/SHOW/GRAPH.

Each one of the four operations will be discussed below.

### Add

Be aware **The tester of this applications purposefully typed Whoops to display error messages after inputs**.
The following inputs are required 1 by 1 from the user:
- Ticker: A ticker available on Yahoo Finance
- Asset Class: A valid Asset Class, incorect input will print the available options which may be entered when prompting is being done again.
- Sector: A valid sector, Invalid input will print the available options after which the user may try again.
- Quantity: A valid positive integer.
- Purchase Price: The purchase price **per unit**

The successfull message indicates that the Asset has been added to the portfolio.

Note, the user may add the same asset multiple times, The quantity and purchase price for all subsequent calls will be stored and will counts towards the total in the portfolio. To add the same ticker twice just follow the same steps again.

**Example session:**

```
Provide a Command (ADD/DELETE/SHOW/GRAPH): ADD
Ticker: Whoops
Whoops does not exist in yahoo finance API

Ticker: ASML
Asset Class: Whoops
Invalid Asset Class, choose one of {All, Digital Assets, Derivatives, Cash & Cash Equivalents, Real Estate, Private Equity, Fixed Income, Equities, Commodities, Hedge Funds, Other}

Asset Class: Equities
Sector: Whoops
Invalid Sector, choose one of {All, Energy, Communication Services, Health Care, Utilities, Real Estate, Information Technology, Materials, Industrials, Other, Consumer Discretionary, Financials, Consumer Staples}

Sector: Information Technology
Quantity: Whoops
Input is not numeric, please provide numeric value.

Quantity: 50
Purchase Price: Whoops
Purchase Price is not numeric, please provide numeric value.

Purchase Price: 200

Successfully added 50 of ASML to the portfolio.
```

### Delete

When the ticker is not present, the tool prints the available tickers to delete.

In the next iteration we see a successfull delete.

The input this operation asks is:

- Ticker: Ticker for an asset.

**Example session:**

```
Provide a Command (ADD/DELETE/SHOW/GRAPH): DELETE
Ticker to delete: Whoops
Ticker not in portfolio, so no deletion.
Delete options: ASML

Provide a Command (ADD/DELETE/SHOW/GRAPH): DELETE
Ticker to delete: ASML
Ticker deleted
...
```

### Show

The Show function has two options. It can either print a summary containing information on the portfolio, such as transactions, values, long names, etc., or it can print the weights or relative weights. Error messages are dynamic, as with the ADD operation, so I will leave these out.

- Summary table

**Example session:**

```
Provide a Command (ADD/DELETE/SHOW/GRAPH): SHOW
Table (Summary or Weights): summary
| Ticker | Asset Name                         | Sector                 | Asset Class | Quantity | Purchase Price | Transaction Value | Current Value |
|--------|------------------------------------|------------------------|-------------|----------|----------------|-------------------|---------------|
| ASML   | ASML Holding N.V.                  | Information Technology | Equities    | [10, 10] | [300.0, 600.0] | 9000              | 21661.42      |
| TSLA   | Tesla, Inc.                        | Consumer Staples       | Equities    | 10       | 300.0          | 3000              | 4451.79       |
| PG     | The Procter & Gamble Company       | Health Care            | Equities    | 10       | 200.0          | 2000              | 1496.3        |
| TLT    | iShares 20+ Year Treasury Bond ETF | Other                  | Fixed Income| 10       | 50.0           | 500               | 905.95        |
```

-  Weights table: See example usage below. Here we see that the Information Technology sector takes up 0.664 or 66.4\% of the total portfolio, thereafter the relative weights w.r.t. to the Information Technology allocation are calculated and displayed. For other options please provide other inputs to **By Asset Class** and/or **By Sector**.

**Example session:**

```
Provide a Command (ADD/DELETE/SHOW/GRAPH): SHOW
Table (Summary or Weights): weights
By Asset Class (all or specific asset class): all
By Sector (all or specific sector): Information Technology

Weight Information Technology w.r.t. total portfolio: 0.664

Information Technology portfolio weights
| Ticker | Weights |
|--------|---------|
| ASML   | 0.8     |
| AAPL   | 0.2     |
```

### Graph

Graph has three options: Individual Assets/Portfolio/Monte Carlo. Individual Assets is the only one independent of the state of the portfolio. In the text box below, I perform two examples.

**Example session:**

```
Provide a Command (ADD/DELETE/SHOW/GRAPH): GRAPH
Type (Individual Assets/Portfolio/Monte Carlo): Individual Assets
Start date for the graph (YYYY-MM-DD): 2015-10-12
End date for the graph (YYYY-MM-DD or None): None
Provide a name for the graph (no extension): example1
Asset tickers (Chain with ,): ASML,MSFT,TSLA,PG,TLT,GOOG

Individual graphs written to graphs/example1.png

Provide a Command (ADD/DELETE/SHOW/GRAPH): GRAPH
Type (Individual Assets/Portfolio/Monte Carlo): Monte Carlo
Start date for the graph (YYYY-MM-DD): 2015-10-12
End date for the graph (YYYY-MM-DD or None): None
Provide a name for the graph (no extension): Monte Carlo
By Asset Class (all or specific asset class): Equities
By Sector (all or specific sector): Information Technology
Number of Simulations: 100000
Number of years (min 1/12, max 100): 15

Monte Carlo graph written to graphs/Monte Carlo.png
```
 I will explain the non intuitive inputs:

- End date: This date is taken as the end date of the historical data and would be the starting point for a monte carlo simulation. If None is used, The tool takes the most recent, available date.
- Asset tickers: Any number of tickers may be chained together using commas like in the text box above. Spaces are fine, however these are postprocessed. Hence, input similar to the example above is preferred.
- In the Monte Carlo case you have the option to also plot a filtered portfolio. This works similarly for the Portfolio graph option and the Weights Table described in [Show](#show).

The plots created in this example can be found in the graphs folder.



## Assumptions and Notes

1. First code specifications: I used type hints and numpy docstrings and tried to conform to a relative extent to pep8. I used an adjusted max width however of 100 for code and 70 for docstrings.
2. When I take historical data of a portfolio, I assume continuous rebalancing. So across the time series, weights stay the same.
3. I assume that the Stock price follows a Geometric Brownian Motion, So that the log returns are normally distributed (can for sure be debated in another project). The time horizon specified for the history is the same horizon I use for the estimates of mu and sigma:  


    $dS_t = \mu S_t \, dt + \sigma S_t \, dW_t$
4. In the Monte Carlo simulation I plot 20 realizations and I plot a few quantiles as well together with the history.
5. I tried to cover edge cases as much as possible but w.r.t. to the deadline and my availability, I didn't cover **everything**.
---

