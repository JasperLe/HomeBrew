"""
Used to insert the MAVG data in the database.
Should be called once a day. AFTER THE TRADING DAY.
"""
import datetime
import pandas_datareader as pdr
import csv
import MySQLdb
import pandas as pd

db = MySQLdb.connect()


def getList():
    index = []
    with open("SPNasdaqAEXXETRA.csv", "r") as f:
        lines = csv.reader(f)
        for i in lines:
            index.append(i[0])
            print(i[0])
    return index


def get_data_to_csv(info):
    print('Getting data from yahoo and appending to csvs')
    db = pdr.get_data_yahoo(info,
                            start=datetime.datetime.now() - datetime.timedelta(days=2),
                            end=datetime.datetime.now())
    print('writing to csvs')
    db['Volume'].to_csv(path_or_buf='YoYinfoVolume.csv', mode='a', header=False)
    db['Low'].to_csv(path_or_buf='YoYinfoLow.csv', mode='a', header=False)
    db['High'].to_csv(path_or_buf='YoYinfoHigh.csv', mode='a', header=False)
    db['Open'].to_csv(path_or_buf='YoYinfoOpen.csv', mode='a', header=False)
    db['Close'].to_csv(path_or_buf='YoYinfoClose.csv', mode='a', header=False)


def get_data_from_csv():
    db_Close = pd.read_csv(filepath_or_buffer='YoYinfoClose.csv', index_col='Date')
    return db_Close


def get_MAVG_data():
    temp = getList()
    get_data_to_csv(temp)


def main():
#    get_MAVG_data()
    cur = db.cursor()
    db_Close = get_data_from_csv()
    ten = db_Close.rolling(window=10).mean()
    fifty = db_Close.rolling(window=50).mean()
    twohundred = db_Close.rolling(window=200).mean()
    cur.execute("TRUNCATE TABLE MAVG")
    for column in twohundred:
        print(column)
        cur.execute("INSERT INTO MAVG (Symbol, 200day, 50day, 10day) VALUES (%s, %s, %s, %s)",
                    (column, float(twohundred[column].tail(1)), float(fifty[column].tail(1)), float(ten[column].tail(1))))
        db.commit()


main()
