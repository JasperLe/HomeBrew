"""
Author: Jasper Lelijveld
Script: Algorithmic Stock Trader (object-oriented)
Date: 11-05-2017
Time spent v0.1: +-6 hours

Python starttime is 13:30

v0.1

It trades stocks... and does this all on its own. Simply start the script and wait.

yahoo allows 2000 calls per hour per ip for non-corporate users so having a 2 second delay after
each check gives me (60*60)/2 = 1800 calls < 2000 -> yahoo won't block me...

Prerequisites:  - A database containing a table of moving average (mavg) data,
                - A script that automatically updates the mavg table after each trading day,
                - A database with a account table, portfolio table and trade table

Current buy/sell determinant:
    - A mavg function: the MAVG_analysis() of each stock object
"""

import MySQLdb
import pandas as pd
from yahoo_finance import Share
import time
import datetime
import sys

"""
The database class. Used for the db connection
Insert your info here
"""
class database:
    def __init__(self):
        self.db = MySQLdb.connect()  # your info here
        self.cur = self.db.cursor()
        self.db.autocommit(True)

"""
The portfolio class. Used to construct the list of stocks CURRENTLY in the portfolio.
"""
class current_portfolio:
    """initialize the portfolio object"""
    def __init__(self, db, cur):
        self.portfolio = pd.read_sql(sql='SELECT * FROM portfolio', con=db)
        self.portfolio = self.portfolio.set_index(self.portfolio['Symbol'])
        self.db = db
        self.cur = cur
    """return price of stock (symbol) in portfolio"""
    def get_portfolio_stock_price(self, symbol):
        return self.portfolio.loc[symbol]['Price']

    """return number of shares of stock (symbol) in portfolio"""
    def get_portfolio_stock_shares(self, symbol):
        return self.portfolio.loc[symbol]['Shares']

    """return target price of stock (symbol) in portfolio"""
    def get_portfolio_target_price(self, symbol):
        return self.portfolio.loc[symbol]['TargetPrice']

    """return list of stocks in portfolio"""
    def stock_list(self):
        return list(self.portfolio['Symbol'])

    """update the portfolio object based on the remote portfolio"""
    def update_object(self):
        self.portfolio = pd.read_sql(sql='SELECT * FROM portfolio', con=self.db)
        self.portfolio = self.portfolio.set_index(self.portfolio['Symbol'])


"""
The stock class. A stock object for each symbol that holds all the relevant information
and functions. Also contains most SQL statements that interact with the remote database
"""
class stock:
    """initialize the stock object"""
    def __init__(self, symbol, cur):
        # the yahoo finance object
        self.object = Share(symbol)
        # the stock symbol
        self.symbol = symbol
        # the stock price
        self.price = float(self.object.get_price())
        # db cursor
        self.cur = cur
        # value of stocks
        self.value = 0
        # number of shares tha can be bought with $1000
        self.shares = int(1000/self.price)
        # moving average 10 days
        self.ten = 0
        # moving average 50 days
        self.fifty = 0
        # moving average 200 days
        self.twohundred = 0
        # target price based on current price and global percentage return
        self.target_price = self.price * (1 + pct)

    """set the number of shares when needed"""
    def set_shares(self, shares):
        self.shares = int(shares)

    """set target price when needed"""
    def set_target_price(self, i):
        self.target_price = i

    """update the price, and value when needed"""
    def update(self):
        print("Updating %s..." % self.symbol)
        self.object.refresh()
        self.price = float(self.object.get_price())
        self.value = self.shares * self.price

    """buy the stock"""
    def buy(self):
        print("Buying %s..." % self.symbol)
        # update to get most recent data
        self.update()
        # insert the stock info in the portfolio sql table
        self.cur.execute("INSERT INTO portfolio (Symbol, Shares, Price, Value, TargetPrice, PriceBought) VALUES (%s, %s, %s, %s, %s, %s)",
                         (self.symbol, self.shares, self.price, self.value, self.target_price, self.price))
        # insert the stock info in the trades sql table
        self.cur.execute("INSERT INTO trades (symbol, price, shares, buyORsold) VALUES (%s, %s, %s, %s)",
                         (self.symbol, self.price, self.shares, "BUY"))
        # get most recent info from account
        self.cur.execute("SELECT * FROM account ORDER BY ind DESC LIMIT 1")
        # update info returned
        info = list(self.cur.fetchone())
        info[2] += self.value
        info[3] -= self.value
        # update account sql table based on the updated info
        self.cur.execute("INSERT INTO account (wealth, stocks, money) VALUES (%s, %s, %s)",
                         (info[2] + info[3], info[2], info[3]))

    """sell the stock"""
    def sell(self):
        print("Selling %s..." % self.symbol)
        # update to get most recent data
        self.update()
        # delete stock from portfolio sql table
        self.cur.execute("DELETE FROM portfolio WHERE Symbol = %s",
                         (self.symbol,))
        # insert the stock info into the trades sql table
        self.cur.execute("INSERT INTO trades (symbol, price, shares, buyORsold) VALUES (%s, %s, %s, %s)",
                         (self.symbol, self.price, self.shares, "SELL"))
        # get most recent info from account
        self.cur.execute("SELECT * FROM account ORDER BY ind DESC LIMIT 1")
        # update info returned
        info = list(self.cur.fetchone())
        info[2] -= self.value
        info[3] += self.value
        # update account sql table based on the updated info
        self.cur.execute("INSERT INTO account (wealth, stocks, money) VALUES (%s, %s, %s)",
                         (info[2] + info[3], info[2], info[3]))

    """set 10 days mavg"""
    def set_ten(self, i):
        self.ten = i

    """set 50 days mavg"""
    def set_fifty(self, j):
        self.fifty = j

    """set 200 days mavg"""
    def set_twohundred(self, k):
        self.twohundred = k

    """analyze the mavg info"""
    def MAVG_analysis(self):
        print("Analyzing %s..." % self.symbol)
        # if it is True you should buy the stock
        if self.twohundred < self.fifty and self.fifty > self.ten and \
                                self.fifty > self.price > self.ten and self.target_price < self.fifty:
            return True
        # if it is False you should sell the stock
        else:
            return False

    def __repr__(self):
        return self.symbol + " $" + str(self.price) + " #" + str(self.shares) + " $" + \
               str(self.value) + " $" + str(self.target_price) + " 10d:" + str(self.ten) + \
               " 50d:" + str(self.fifty) + " 200d:" + str(self.twohundred)


"""
MAVG class. The mavg database object with the relevant functions. Based on pandas dataframe
workings.
"""
class MAVG:
    """get mavg data from sql table"""
    def __init__(self, db):
        self.MAVG = pd.read_sql(sql="SELECT * FROM MAVG", con=db)
        self.MAVG = self.MAVG.set_index(self.MAVG['Symbol'])

    """return list of symbols in mavg table"""
    def MAVG_symbols(self):
        return list(self.MAVG['Symbol'])

    """return 10 days mavg of symbol"""
    def stock_MAVG_ten(self, symbol):
        return self.MAVG.loc[symbol]['10day']

    """return 50 days mavg of symbol"""
    def stock_MAVG_fifty(self, symbol):
        return self.MAVG.loc[symbol]['50day']

    """return 200 days mavg of symbol"""
    def stock_MAVG_twohundred(self, symbol):
        return self.MAVG.loc[symbol]['200day']

"""
A function that creates a list of stocks of the inserted list
Used for CURRENT stocks

I expect an http/sqlerror with the yahoo_finance library about every 100 calls.
I expect no errors with a 10 stock portfolio it tries the whole portfolio at once
"""
def current_stocks_list():
    portfolio_stock_list = []
    while True:
        try:
            for i in portfolio.stock_list():
                # create the stock object
                temp = stock(i, database.cur)
                # sat shares
                temp.set_shares(portfolio.get_portfolio_stock_shares(i))
                # set targetprice
                temp.set_target_price(portfolio.get_portfolio_target_price(i))
                # set 10 days mavg
                temp.set_ten(mavg.stock_MAVG_ten(temp.symbol))
                # set 50 days mavg
                temp.set_fifty(mavg.stock_MAVG_fifty(temp.symbol))
                # set 200 days mavg
                temp.set_twohundred(mavg.stock_MAVG_twohundred(temp.symbol))
                # append stock to list
                portfolio_stock_list.append(temp)
            break
        except:
            print("Retry!!")
            continue
    return portfolio_stock_list, portfolio.stock_list()

"""
A function that creates a list of stocks of the inserted list
Used for ALL stocks not in CURRENT

I expect an http/sqlerror with the yahoo_finance library about every 100 calls.
I expect at least 1 error in the whole list so each stock is tried separately
Each failure is append to the errors list
"""
def all_stocks_list(stocks):
    all_stock_list = []
    errors = []
    for i in stocks:
        try:
            # create stock object
            temp = stock(i, database.cur)
            # set 10 day mavg
            temp.set_ten(mavg.stock_MAVG_ten(temp.symbol))
            # set 50 days mavg
            temp.set_fifty(mavg.stock_MAVG_fifty(temp.symbol))
            # set 200 days mavg
            temp.set_twohundred(mavg.stock_MAVG_twohundred(temp.symbol))
            print(temp)
            # append to list
            all_stock_list.append(temp)
        except:
            print("Something went wrong with %s..." % i)
            errors.append(i)
            continue
    return all_stock_list


"""checks whether the predetermined amount of time has passed and quits if True"""
def quit():
    if time.time() - starttime > offset:
        sys.exit()

"""
The main function for trading:
By moving stocks from all -> current and current -> all determine what is in and out of portfolio
"""
def main(list_current, list_new):
    print("Starting trading @ %s" % datetime.datetime.now())
    # loopdiloop (not the right way to do it...)
    while True:
        # checks current list len to determine whether we should update current stocks of look for new stocks
        # True is current
        # False is look for new
        if len(list_current) == 10:
            # repeat for stocks in list...
            for i in range(len(list_current)):
                # try checken whether the buy/sell condition is True or False
                try:
                    list_current[i].update()
                    # if False, sell stock and move stock to all_list
                    if list_current[i].MAVG_analysis() is False:
                        list_current[i].sell()
                        portfolio.update_object()
                        list_new.append(list_current.pop(i))
                        break
                    # if True continue
                except:
                    print("Something went wrong with %s..." % list_current[i].symbol)
                # check time passed
                quit()
                # sleep 2 seconds to prevent yahoo from blocking my ip
                time.sleep(2)
        # look in all list for good stocks
        else:
            # repeat for all stocks in list
            for i in range(len(list_new)):
                # try checking
                try:
                    list_new[i].update()
                    # if True
                    # buy stock and move to current list
                    if list_new[i].MAVG_analysis() is True:
                        list_new[i].buy()
                        portfolio.update_object()
                        list_current.append(list_new.pop(i))
                        break
                    # if False continue
                except:
                    print("Something went wrong with %s..." % list_new[i].symbol)
                # check time again
                quit()
                # sleep 2 seconds
                time.sleep(2)

"""
The script: - create db connection,
            - create portfolio,
            - create mavg,
            - make portfolio list AND all stocks list
            - start trading
"""
print("Starting Trader @ %s..." % datetime.datetime.now())
starttime = time.time()
# script should run a maximum of 24000 seconds which equals one trading day
# and about 20 minutes of startup time
offset = 24000
pct = 0.03
# create global variables (it does not need to be safe)
# it is build like this so we do not need to pass all these variables constantly
database = database()
portfolio = current_portfolio(database.db, database.cur)
mavg = MAVG(database.db)
in_portfolio_stocks, in_portfolio_symbols = current_stocks_list()
all_symbols = mavg.MAVG_symbols()
all_symbols_excluding_portfolio = [item for item in all_symbols if item not in in_portfolio_symbols]
new_stocks_list = all_stocks_list(all_symbols_excluding_portfolio)
# start the main function
main(in_portfolio_stocks, new_stocks_list)
