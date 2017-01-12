import pandas as pd
import datetime
from pandas_datareader import data as web

# We will look at stock prices over the past year, starting at January 1, 2016
start = datetime.datetime(2016, 1, 1)
end = datetime.datetime(2016, 12, 31)

# Let's get Apple stock data; Apple's ticker symbol is AAPL
# First argument is the series we want, second is the source ("yahoo" for Yahoo! Finance), third is the start date, fourth is the end date
apple = web.DataReader("BVB", "yahoo", start, end)
microsoft = web.DataReader("ARL", "yahoo", start, end)
google = web.DataReader("BNR", "yahoo", start, end)

stocks = pd.DataFrame({"BVB": apple["Adj Close"],
                        "ARL": microsoft["Adj Close"],
                        "BNR": google["Adj Close"]})

print stocks.head()


def stockSelector():
    temp = web.DataReader("yahoo", start, end)
    print temp

