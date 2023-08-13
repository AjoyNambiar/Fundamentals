from flask import Flask, render_template
from flask import request
from datetime import datetime
from yahoofinancials import YahooFinancials
import pandas as pd


year = datetime.now().year


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
    print("success")
    return test_stock_df


app = Flask(__name__)

@app.route('/')
def home():
    return render_template("index.html", year=year)

@app.route('/estimate/<ticker>/<expected_return>/<exit_pe>')
def estimate(ticker, expected_return, exit_pe):
    df = PEValueEstimate(ticker,expected_return ,exit_pe )
    print(df)
    return render_template("estimate.html", test_stock_df=df)

@app.route('/estimator_page', methods=['GET', 'POST'])
def receive_data():
    user_ticker = request.form['user_ticker']
    print(user_ticker)
    user_expected_return = float(request.form['user_expected_return'])/100  #convert % to float
    print(user_expected_return)
    user_exit_pe = float(request.form['user_exit_pe'])

    try:
        return estimate(user_ticker, user_expected_return, user_exit_pe)
    except Exception as e:
        print("error1")
        #logging.error(e, exc_info=False)

        #return f"<h1> {log} </h1>"



if __name__ == "__main__":
    app.run(debug=True)


