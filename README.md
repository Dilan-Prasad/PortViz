# Portfolio Visualization and Analysis

## Graph Generation Script

### Description

The PortViz program provides a rich visual representation of your stock portfolio's performance over the past 5 years. It allows you to:

- Compare your portfolio's performance against the S&P 500 index to see if you're outperforming or underperforming the market.
- See the overall value of your portfolio and how it changes over time.
- Track the performance of each individual stock within your portfolio.

#### Technical Details

1. **Data Extraction**: Extracts tickers, quantities, and average buy prices for each stock from the `stocks` list.
2. **Data Download**: Downloads historical data for all specified tickers over the last 5 years using the `yfinance` library.
3. **Portfolio DataFrame**: Prepares a DataFrame to store the portfolio values over time.
4. **Value Calculation**: Calculates the value of each holding and adds it to the DataFrame.
5. **Data Filling**: Fills missing dates to avoid gaps in the graph.
6. **Total Portfolio Value**: Sums the individual stock values to get the total portfolio value.
7. **S&P 500 Data**: Downloads historical S&P 500 data and scales it to match the initial value of the portfolio.
8. **Graph Creation**: Uses Plotly to create a graph with the following features:
    - Lines representing the overall portfolio value and each individual stock's performance.
    - A solid black line representing the S&P 500, scaled to fit the portfolio range.
    - Vertical dashed red lines at the start of each year for better visualization.
    - Customized layout to remove horizontal grid lines.

### Example Usage
##### In stocks.json:

```json
[
    {"ticker": "AAPL", "avg_buy_price": 150, "quantity": 10},
    {"ticker": "GOOGL", "avg_buy_price": 1200, "quantity": 5},
    {"ticker": "MSFT", "avg_buy_price": 200, "quantity": 8}
]
```

##### Run command:
```
python3 PortViz.py
```

##### Output:
```
Portfolio Summary:

Total Portfolio Performance: $X,XXX.XX -> $Y,YYY.YY = $ZZZ.ZZ +XX.XX%

Ticker                       Initial Amount     Current Amount     Amount Change    Percent Change
______                       ______________     ______________     _____________    ______________

 GOOGL         60.00%         $6,000.00         $6,500.00           +$500.00              +8.33%
 AAPL          15.00%         $1,500.00         $1,700.00           +$200.00             +13.33%
 MSFT          16.00%         $1,600.00         $1,800.00           +$200.00             +12.50%
``````




