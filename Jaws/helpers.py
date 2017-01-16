import csv
import pandas as pd
import datetime
from pandas_datareader import data as web

# learning
import numpy as np
import matplotlib.pyplot as plt
from matplotlib import style
style.use("ggplot")
from sklearn import svm
import sklearn.metrics as met
import sklearn.covariance as cov


# define timeperiod
start = datetime.datetime(2016, 1, 4)
end = datetime.datetime(2016, 12, 31)


def getList():
    index = []
    with open("SPNasdaq.csv", "rb") as f:
        lines = csv.reader(f)
        for i in lines:
            index.append(i[0])
    return index


# Main portfolio loop
def getStockData():
    # get ticker list from csv
    ticker_list = getList()
    # get info for tickers from Yahoo and store in df
    StockPriceYeardf = pd.DataFrame()
    for i in ticker_list:
        try:
            stock = web.DataReader(i, "yahoo", start, end)
        except:
            print i, ": FAILED"
            continue
        StockPriceYeardf[i] = stock["Adj Close"]
        print i
    StockChangeFromBaseYeardf = getLogChange(StockPriceYeardf)

    evaluator(StockChangeFromBaseYeardf)

# Returns change compared to a base
def getChangeFromBase(x):
    return x.apply(lambda x: x/x[0]).fillna(value=1)

# Returns log change
def getLogChange(x):
    return x.apply(lambda x: np.log(x) - np.log(x.shift(1)))


def evaluator(x):
    change = 0
    money = 100
    list = []
    listChange = []
    listMoney = []
    logChange = []

    counter = 0
    c = 0
    for i in x.values:
        j = i[c]
        if max(i) > j:
            change += 1
        elif max(i) < j:
            change -= 1
        if change == 4:
            for k in range(len(i)):
                if i[k] == max(i):
                    h = k
        if change == 5:
            c = h
            money = money*(1+i[c])
            change = 0
        elif change >= 0 and counter > 0:
            money = money*(1+i[c])
        counter += 1

        # data collection
        logChange.append(i[c])
        list.append([x.columns[c],c])
        listChange.append(change)
        listMoney.append(money)
    # dataframe builder
    ch = pd.Series(listChange, name='Change')
    li = pd.Series(list, name='Stock')
    lm = pd.Series(listMoney, name='Total')
    lc = pd.Series(logChange, name='Change of stock invested')
    left = pd.DataFrame(ch)
    left = pd.concat([left, li], axis=1)
    left = pd.concat([left, lm], axis=1)
    left = pd.concat([left, lc], axis=1)
    x = x.reset_index()
    result = pd.concat([left, x], axis=1)
    result = result.set_index(['Date'])
    # csv writer and print
#    result.to_csv('output.csv')
    X, y = transform(x)
    cov_array = pd.DataFrame(cov.empirical_covariance(X, assume_centered=False))
#    cov_array.to_csv('Cov_array.csv')
    learn(X, y)

#    y_true, y_pred = correlationDF(X)
#    print met.matthews_corrcoef(y_true,y_pred)

#    print result

# based on 2 stocks.
def transform(x):
    x = x.fillna(value=1)
    X = x.as_matrix(columns=x.columns[1:])
    y = []
    for i in range(len(X)):
        a = []
        for j in range(10):
            if X[i][j] > 0:
                a.append(1)
            else:
                a.append(-1)
        if sum(a) == 2:
            y.append(1)
        elif sum(a) == 0:
            y.append(0)
        else:
            y.append(-1)
    return X, y


def learn(X, y):
    clf = svm.SVC(kernel='linear', C=1.0, probability=True)
    quarter = len(X)/4

    clf.fit(X[0:len(X)-quarter],y[0:len(y)-quarter])
    data = np.array(X[-quarter:]*100)
    prediction = clf.predict(data)
    print prediction

def correlationDF(X):
    y_true = []
    y_pred = []
    for i in range(10):
        for j in range(len(X)):
            if X[j][i] > 0:
                if i == 0:
                    y_true.append(1)
                else:
                    y_pred.append(1)
            else:
                if i == 0:
                    y_true.append(-1)
                else:
                    y_pred.append(-1)
    print y_true,y_pred
    return y_true,y_pred


getStockData()
