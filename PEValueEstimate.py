from yahoofinancials import YahooFinancials
import pandas as pd


def PEValueEstimate(ticker='AAPL', expected_return=0.05, exit_pe=15.0):
    yahoofinancials = YahooFinancials(ticker)

    stock_price = yahoofinancials.get_open_price()
    pe_ratio = yahoofinancials.get_pe_ratio()
    eps = stock_price / pe_ratio
    ten_yr_stock_price = stock_price * (1 + float(expected_return)) ** 10
    ten_yr_eps = ten_yr_stock_price / float(exit_pe)
    implied_eps_cagr = (ten_yr_eps / eps) ** (1 / 10) - 1
    dividend_yield = yahoofinancials.get_dividend_yield()

    test_stock = {
        "Stock Price": [round(stock_price, 2)],
        "EPS": [round(eps, 2)],
        "PE Ratio": [round(pe_ratio, 2)],
        "Expected 10 YR CAGR Return%": [float(expected_return) * 100],
        "Dividend Yield": [dividend_yield * 100],
        "10 Yr Forward Stock Price": [round(ten_yr_stock_price, 0)],
        "Exit P/E": [exit_pe],
        "10 Yr Forward EPS": [round(ten_yr_eps, 2)],
        "Implied EPS CAGR%": [round(implied_eps_cagr * 100, 2)],
    }
    test_stock_df = pd.DataFrame(test_stock).T.round(decimals=2)
    test_stock_df.columns = [ticker]
    return test_stock_df
