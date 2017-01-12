import csv
import random
import matplotlib.pyplot as plt
import matplotlib.animation as animation
import pandas as pd
import datetime
from pandas_datareader import data as web

# globals for animation
counter = 0
t = [0]

# a random portfolio/weight generator based on a csv with ticker,company names
# returns a list with a [ticker, name], weigth
# scales based on csv length and dollar amount
def randomRoller(a, b):
    index = getList()
    portfolio = []
    total = 0.0
    maximum = 0
    for k in range(a):
        x = []
        i = random.randint(0, len(index)-1)
        j = random.randint(1, a)
        total += j
        if i not in portfolio:
            x.append(index[i])
            x.append(j)
            portfolio.append(x)
    for i in portfolio:
        temp = b/total
        i[1] *= temp
        maximum += i[1]
    return portfolio

# gets list of ticker,companies
def getList():
    index = {}
    e = 0
    with open("SPNasdaqAEXXETRA.csv", "rb") as f:
        lines = csv.reader(f)
        for i in lines:
            index[e] = [i[0], i[1]]
            e += 1
    return index

# Main portfolio loop
def createPortfolio(a,b):
    # define timeperiod
    start = datetime.datetime(2016, 1, 4)
    end = datetime.datetime(2016, 12, 31)

    # get info for randomly made portfolio from Yahoo
    portfolio = randomRoller(a,b)
    listed = pd.DataFrame()
    for i in portfolio:
        j = i[0]
        ticker = j[0]
        try:
            stock = web.DataReader(ticker, "yahoo", start, end)
        except:
            print ticker
            continue
        listed[ticker] = stock["Adj Close"]

    # perform calculations/manipulations
    stock_return = listed.apply(lambda x: x/x[0]).fillna(value=1)
    stock_return["Sum"] = stock_return.sum(axis=1).divide(10)
    stock_change = listed.apply(lambda x: (x[len(x)-1] - x[0])/x[0]).fillna(value=0)
    # change Series in Dataframe
    left = stock_change.to_frame(name='Change')
    left['Tickers'] = stock_change.index

    # get weights from portfolio
    weighted = []
    for i in portfolio:
        weighted.append(i[1])
    # create Series
    se = pd.Series(weighted, name='Weight')
    # transfrom to Dataframe (This isn't the correct way to do this, but works)
    right = se.to_frame()
    right['Tickers'] = stock_change.index
    # merge two dataframes for complete dataframe
    result = pd.merge(left, right, on=['Tickers'])
    # perform weighting at total change
    result['Weighted Change'] = result['Change']*result['Weight']
    result = result[['Tickers', 'Change', 'Weight', 'Weighted Change']]
    total_change = sum(result['Weighted Change'])
    weighted_return = pd.DataFrame()
    # perform weighting for complete dataframe (used for the animation)
    for i in range(10):
        weighted_return[[i]] = stock_return[[i]].apply(lambda x: x*result['Weight'][i])
    weighted_return.columns = result["Tickers"]
    weighted_return["Sum"] = weighted_return.sum(axis=1)
    result.loc[10] = ["Total profit:", "xxx", "xxx", total_change]
    # Animate/plot the change of the portfolio during the year
    # plot the change for each stock
    # Animata works for one portfolio, needs change for multiple portfolio compatibility
#    animata(stock_return, listed, weighted_return)
    return result


def animata(stock_return, listed, weighted_return):
    stock_return.plot(grid=True).axhline(y=1, color="black", lw=1)
    listed.plot(grid=True)
    fig = plt.figure()
    ax1 = fig.add_subplot(1, 1, 1)
    frames = len(weighted_return)-2
    print frames
    data = list(weighted_return["Sum"])
    price = [data[1]]
    def animate(i):
        global t, counter
        x = t
        y = price
        counter += 1
        if counter > len(weighted_return["Sum"]):
            print "boe"
        x.append(counter)
        y.append(data[counter])
        ax1.clear()
        plt.plot(x, y, color="blue")
    ani = animation.FuncAnimation(fig, animate, interval=50, frames=frames, repeat=False)

    plt.show()
