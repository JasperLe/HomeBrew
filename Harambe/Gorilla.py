from helpers import *
import pandas as pd


def monkeyTime():
    print "Hey! Wanna make a random portfolio?"
    b = input("How many dollars can you spend?: ")
    c = input("How many portfolios do you want to generate?: ")
    vector = pd.DataFrame()
    for repeat in range(int(c)):
        temp = createPortfolio(10,int(b))
        # for concating one biiiiig dataframe
#        vector = pd.concat([vector, temp], axis=1)
        print temp, "\n"
#    print vector


monkeyTime()
