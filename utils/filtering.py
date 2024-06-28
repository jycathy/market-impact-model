import numpy as np
import pandas as pd

def compute_daily_vol(return_df):
    # compute daily volatility
    window_size = int(6.5 * 30)
    stds = []
    
    return_df.fillna(0, inplace=True)
    
    for index, row in return_df.iterrows():
        # Calculate rolling standard deviation with the specified window size
        rolling_std = row.rolling(window=window_size).std()
        # Scale the standard deviation to daily values
        scaled_std = rolling_std * np.sqrt(195)
        stds.append(scaled_std)
    
    # Concatenate the list of scaled standard deviations into a DataFrame
    volatility_df = pd.concat(stds, axis=1)
    volatility_df.columns = return_df.index  # Assign column names as stock symbols
    volatility_df.fillna(0, inplace=True)

    daily_vol = []
    for i in range(0, len(volatility_df), 195):
        # Extract volatility values within the current range
        range_volatility = volatility_df.iloc[i:i+195]
        # Calculate the average volatility for each day (row) in the range
        daily_volatility = range_volatility.mean()
        # Calculate the mean volatility for the entire range
        daily_vol.append(daily_volatility)

    return np.array(daily_vol).T

def filter_high_vol_days(daily_vol, percentile_threshold=95):
    filtered_days = []

    daily_vol = np.mean(daily_vol, axis=0)

    threshold = np.percentile(daily_vol, 95)

    filtered_days = np.where(daily_vol <= threshold)[0]

    return filtered_days


# get the indicies after filtering high volatility days
midQuoteReturnsArrayDf = pd.read_csv("output/midQuoteReturnsArrayDf.csv", index_col=0)
daily_vol = compute_daily_vol(midQuoteReturnsArrayDf)
filtered_indices = filter_high_vol_days(daily_vol)

totalDailyValueDf = pd.read_csv("output/totalDailyValueDf.csv",index_col=0)
imbalanceDf = pd.read_csv("output/imbalanceDf.csv",index_col=0)
vwap330Df = pd.read_csv("output/vwap330Df.csv",index_col=0)
vwapCloseDf = pd.read_csv("output/vwapCloseDf.csv",index_col=0)
arrivalPriceDf = pd.read_csv("output/arrivalPriceDf.csv",index_col=0)
terminalPriceDf = pd.read_csv("output/terminalPriceDf.csv",index_col=0)

midQuoteReturnsArrayDf = midQuoteReturnsArrayDf.iloc[:, filtered_indices]
totalDailyValueDf = totalDailyValueDf.iloc[:, filtered_indices]
imbalanceDf = imbalanceDf.iloc[:, filtered_indices]
vwap330Df = vwap330Df.iloc[:, filtered_indices]
vwapCloseDf = vwapCloseDf.iloc[:, filtered_indices]
arrivalPriceDf = arrivalPriceDf.iloc[:, filtered_indices]
terminalPriceDf = terminalPriceDf.iloc[:, filtered_indices]
daily_vol =  pd.DataFrame(daily_vol).iloc[:, filtered_indices]

midQuoteReturnsArrayDf.to_csv("input/midQuoteReturnsArrayDf.csv", index_label="Stock")
totalDailyValueDf.to_csv("input/totalDailyValueDf.csv", index_label="Stock")
imbalanceDf.to_csv("input/imbalanceDf.csv", index_label="Stock")
vwap330Df.to_csv("input/vwap330Df.csv", index_label="Stock")
vwapCloseDf.to_csv("input/vwapCloseDf.csv", index_label="Stock")
arrivalPriceDf.to_csv("input/arrivalPriceDf.csv", index_label="Stock")
terminalPriceDf.to_csv("input/terminalPriceDf.csv", index_label="Stock")
daily_vol.to_csv("input/dailyVolDf.csv", index_label="Stock")
