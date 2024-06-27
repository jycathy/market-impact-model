import os
import numpy as np
import pandas as pd
from tqdm import tqdm

from taq import MyDirectories
from taq.TAQTradesReader import TAQTradesReader
from taq.TAQQuotesReader import TAQQuotesReader
from impactUtils.FirstPriceBuckets import FirstPriceBuckets
from impactUtils.LastPriceBuckets import LastPriceBuckets
from impactUtils.MidQuoteReturnBuckets import MidQuoteReturnBuckets
from impactUtils.VWAP import VWAP
from impactUtils.ImbalanceValue import *
from impactUtils.DailyValue import *

# Read the list of S&P 500 stock symbols from the file
sp500_file_path = 'utils/SP500.txt'
with open(sp500_file_path, 'r') as file:
    sp500_stocks = [line.rstrip() for line in file]
sp500_stocks = [element for element in sp500_stocks if element]

startTS = 19 * 60 * 60 * 1000 / 2
impactTS = 31 * 60 * 60 * 1000 / 2
endTS = 16 * 60 * 60 * 1000

trades_dir = MyDirectories.getTradesDir()
quotes_dir = MyDirectories.getQuotesDir()

trades_reader = TAQTradesReader
quotes_reader = TAQQuotesReader

num_of_stocks = len(sp500_stocks)      # 508 stocks
num_of_days = len(os.listdir(MyDirectories.getTradesDir()))     # 65 days
dates = sorted(os.listdir(MyDirectories.getTradesDir()))
assert(len(dates) == 65)

# 2-minute mid-quote returns
midQuoteReturns = []
# total daily value
totalDailyValue = []
# arrival price
arrivalPrice = []
# value imbalance between 9:30 and 3:30
imbalance = []
# volume-weighted average price between 9:30 and 3:30
vwap330 = []
# volume-weighted average price between 9:30 and 4:00
vwap400 = []
# terminal price at 4:00
terminalPrice = []

for date in tqdm(dates):

    mqr_daily = []
    tdv_daily = []
    imb_daily = []
    vwap330_daily = []
    vwap400_daily = []
    arrival_daily = []
    terminal_daily = []

    for stock in sp500_stocks:
        quotes_path = os.path.join(quotes_dir, date, stock + '_quotes.binRQ')
        trades_path = os.path.join(trades_dir, date, stock + '_trades.binRT')
        if os.path.exists(quotes_path) and os.path.exists(trades_path):
            trades = TAQTradesReader(trades_path)
            quotes = TAQQuotesReader(quotes_path)

        # mid-quote returns
        returnBuckets = MidQuoteReturnBuckets(
                    quotes,
                    numBuckets = int((endTS - startTS) / (2.0 * 60 * 1000)),    # 2 minutes
                    startTS = startTS,
                    endTS = endTS
                )
        mqr_daily.append(np.array(returnBuckets._midReturns, dtype=float))

        # total daily value
        tdv_daily.append(getDailyValue(trades, startTS, endTS))
        # imbalance value
        imb_daily.append(getImbalance(trades, startTS, impactTS))
        # vwap ends at 3:30
        vwap330_daily.append(VWAP(trades, startTS, impactTS).getVWAP())
        # vwap ends at 4:00
        vwap400_daily.append(VWAP(trades, startTS, endTS).getVWAP())
        # arrival price
        firstPrice = FirstPriceBuckets(trades, numBuckets=1, startTS=startTS, endTS=endTS)
        arrival_daily.append(firstPrice.getPrice(0)) 
        # terminal price
        lastPrice = LastPriceBuckets(trades, numBuckets=1, startTS=startTS, endTS=endTS)
        terminal_daily.append(lastPrice.getPrice(0))
    
    midQuoteReturns.append(mqr_daily)
    totalDailyValue.append(tdv_daily)
    imbalance.append(imb_daily)
    vwap330.append(vwap330_daily)
    vwap400.append(vwap400_daily)
    arrivalPrice.append(arrival_daily)
    terminalPrice.append(terminal_daily)

concatenated_array = np.concatenate(midQuoteReturns, axis=1)
midQuoteReturns = np.reshape(concatenated_array, (concatenated_array.shape[1], -1)).T
totalDailyValue = np.array(totalDailyValue).T
imbalance = np.array(imbalance).T
vwap330 = np.array(vwap330).T
vwap400 = np.array(vwap400).T
arrivalPrice = np.array(arrivalPrice).T
terminalPrice = np.array(terminalPrice).T

print("midQuoteReturnsArray:", midQuoteReturns.shape)
print("Total Daily Value:",totalDailyValue.shape)
print("Imbalance:", imbalance.shape)
print("VWAP Impact:", vwap330.shape)
print("VWAP Close:", vwap400.shape)
print("Arrival Price:",arrivalPrice.shape)
print("Terminal Price:", terminalPrice.shape)
        
midQuoteReturnsDf = pd.DataFrame(midQuoteReturns, index=sp500_stocks)
totalDailyValueDf = pd.DataFrame(totalDailyValue, index=sp500_stocks)
imbalanceDf = pd.DataFrame(imbalance, index=sp500_stocks)
vwap330Df = pd.DataFrame(vwap330, index=sp500_stocks)
vwapCloseDf = pd.DataFrame(vwap400, index=sp500_stocks)
arrivalPriceDf = pd.DataFrame(arrivalPrice, index=sp500_stocks)
terminalPriceDf = pd.DataFrame(terminalPrice, index=sp500_stocks)

midQuoteReturnsDf.to_csv(os.path.join(MyDirectories.getOutputDir(), "midQuoteReturnsArrayDf.csv"), index_label="Stock")
totalDailyValueDf.to_csv(os.path.join(MyDirectories.getOutputDir(), "totalDailyValueDf.csv"), index_label="Stock")
imbalanceDf.to_csv(os.path.join(MyDirectories.getOutputDir(), "imbalanceDf.csv"), index_label="Stock")
vwap330Df.to_csv(os.path.join(MyDirectories.getOutputDir(), "vwap330Df.csv"), index_label="Stock")
vwapCloseDf.to_csv(os.path.join(MyDirectories.getOutputDir(), "vwapCloseDf.csv"), index_label="Stock")
arrivalPriceDf.to_csv(os.path.join(MyDirectories.getOutputDir(), "arrivalPriceDf.csv"), index_label="Stock")
terminalPriceDf.to_csv(os.path.join(MyDirectories.getOutputDir(), "terminalPriceDf.csv"), index_label="Stock")