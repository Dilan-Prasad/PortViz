import yfinance as yf
import pandas as pd
import plotly.graph_objects as go
from json import load

def load_stocks(filename):
    with open(filename, 'r') as file:
        return load(file)

def plot_portfolio_over_time(stocks):
    # Extract tickers and quantities
    tickers = [stock['ticker'] for stock in stocks]
    quantities = {stock['ticker']: stock['quantity'] for stock in stocks}
    avg_buy_prices = {stock['ticker']: stock['avg_buy_price'] for stock in stocks}
    
    # Download historical data for all tickers at once
    data = yf.download(tickers, period='5y', progress=False)
    
    # Prepare portfolio DataFrame
    portfolio_df = pd.DataFrame(index=data['Close'].index)
    
    # Calculate the value of each holding and add to portfolio DataFrame
    for ticker in tickers:
        portfolio_df[f'Value_{ticker}'] = data['Close'][ticker] * quantities[ticker]

    # Fill missing dates forward to avoid gaps in the graph
    portfolio_df = portfolio_df.ffill()

    # Sum the values to get the total portfolio value
    portfolio_df['Total Value'] = portfolio_df.sum(axis=1)

    # Download S&P 500 data
    sp500 = yf.download('^GSPC', start=portfolio_df.index[0], end=portfolio_df.index[-1], progress=False)
    sp500 = sp500['Close']
    
    # Scale S&P 500 to match the range of the portfolio values
    sp500_scaled = sp500 * (portfolio_df['Total Value'].iloc[0] / sp500.iloc[0])

    # Create the plot with Plotly
    fig = go.Figure()

    # Calculate current values and percentage changes
    current_values = [
        (
            ticker, 
            avg_buy_prices[ticker] * quantities[ticker],
            data['Close'][ticker].iloc[-1] * quantities[ticker],
            ((data['Close'][ticker].iloc[-1] - avg_buy_prices[ticker]) / avg_buy_prices[ticker]) * 100
        )
        for ticker in tickers
    ]

    # Calculate total current portfolio value
    total_portfolio_value = sum(value for _, _, value, _ in current_values)

    # Sort the stocks by current value in descending order
    current_values.sort(key=lambda x: x[2], reverse=True)

    # Add a line for the overall portfolio value
    fig.add_trace(go.Scatter(
        x=portfolio_df.index,
        y=portfolio_df['Total Value'],
        mode='lines',
        name='Portfolio Value',
        hoverinfo='text',
        hovertemplate='$%{y:,.2f}'
    ))

    # Add lines for each individual stock's performance, sorted by current value
    for ticker, _, current_value, _ in current_values:
        portfolio_percentage = (current_value / total_portfolio_value) * 100
        fig.add_trace(go.Scatter(
            x=portfolio_df.index,
            y=portfolio_df[f'Value_{ticker}'],
            mode='lines',
            name=f'{ticker} ({portfolio_percentage:.2f}%)',
            hoverinfo='text',
            hovertemplate='$%{y:,.2f}'
        ))

    # Add a solid black line for the S&P 500
    fig.add_trace(go.Scatter(
        x=sp500_scaled.index,
        y=sp500_scaled,
        mode='lines',
        name='S&P 500',
        line=dict(color='black', width=2),
        hoverinfo='text',
        hovertemplate='$%{y:,.2f}'
    ))

    # Add vertical lines at the start of each year, skipping the first if needed
    start_year = portfolio_df.index[0].year
    if portfolio_df.index[0].month != 1 or portfolio_df.index[0].day != 1:
        start_year += 1  # Skip the first year if it doesn't start on January 1

    for year in range(start_year, portfolio_df.index[-1].year + 1):
        fig.add_shape(
            dict(
                type="line",
                x0=pd.Timestamp(f'{year}-01-01'),
                y0=0,
                x1=pd.Timestamp(f'{year}-01-01'),
                y1=1,
                xref='x',
                yref='paper',
                line=dict(color='red', dash='dash')
            )
        )

    fig.update_layout(
        title='Stock Portfolio Over Time vs S&P 500',
        xaxis_title='Date',
        yaxis_title='Value ($)',
        hovermode='x',
        xaxis_rangeslider_visible=False,
        yaxis=dict(showgrid=True),
        xaxis=dict(showgrid=False)    
    )
    
    fig.show()

    return current_values


def print_stock_info(stocks):
    # Print current values and percentage changes
    total_portfolio_value = sum(value for _, _, value, _ in stocks)
    total_initial_value = sum(value for _, value, _, _ in stocks)

    print("\nPortfolio Summary:\n")
    sign = "+"
    if total_portfolio_value - total_initial_value < 0:
        sign = "-"
    print(f"Total Portfolio Performance: ${total_initial_value:,.2f} -> ${total_portfolio_value:,.2f} = {sign}${abs(total_portfolio_value - total_initial_value):,.2f} [{sign}{abs(100 * (total_portfolio_value - total_initial_value) / (total_initial_value)):.2f}%]\n")

    # Print the titles
    print(f"{'Ticker':<17} {'Initial Amount':>15} {'Current Amount':>17} {'Amount Change':>16} {'Percent Change':>17}")
    print(f"{'______':<17} {'______________':>15} {'______________':>17} {'_____________':>16} {'______________':>17}\n")

    
    # Print the values
    for ticker, initial_investment, current_value, percent_change in stocks:
        portfolio_percentage = (current_value / total_portfolio_value) * 100

        amount_change = current_value - initial_investment

        initial_investment = f"${initial_investment:,.2f}"
        current_value = f"${current_value:,.2f}"

        portfolio_percentage = f"{portfolio_percentage:.2f}%"

        if amount_change >= 0:
            amount_change_str = f"+${amount_change:,.2f}"
        else:
            amount_change_str = f"(${abs(amount_change):,.2f})"
        
        if percent_change >= 0:
            percent_change_str = f"+{percent_change:,.2f}%"
        else:
            percent_change_str = f"({abs(percent_change):,.2f}%)"
        
        print(f" {ticker:<5} "
              f"{portfolio_percentage:>10}"
              f"{initial_investment:>15} "
              f"{current_value:>17} "
              f"{amount_change_str:>16} "
              f"{percent_change_str:>17}")

        
stocks = load_stocks("./stocks.json")
print_stock_info(plot_portfolio_over_time(stocks))