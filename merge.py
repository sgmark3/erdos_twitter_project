import time
import csv
import pandas as pd
import numpy as np
#import concurrent.futures
import itertools
from itertools import compress
import multiprocessing as mp
from datetime import datetime

global DT1, DT2, df_stock, df_tweet, snp500

df_stock = pd.read_csv("/home1/sgmark/networks/erdos_twitter_project/stock_merged.csv")
df_tweet = pd.read_csv("/home1/sgmark/networks/erdos_twitter_project/tweets_temporal_ticker.csv")
DT1 = [0, 250000]
DT2 = [300000, 500000]


def aggregate_time_delayed_stock_data(df_stock, df_tweet, DT1, DT2):
    # This function for tweets and assets already identified to be the same company
    stock_list = []
    df_stocks= df_stock.copy().sort_values(by=['time'])
    for i in df_tweet.index:
        # Get the time associated with an individual tweet
        date_and_time = df_tweet.loc[i,'time_stamp']
        df_stocks_stocks = df_stocks[df_stocks['time']>= date_and_time]
        df_stocks_stocks['delta'] = df_stocks_stocks['time'].copy().apply(lambda x: (datetime.fromisoformat(x)-datetime.fromisoformat(date_and_time)).total_seconds())
        try:
            # Get prices that lie within buying and selling time differential
            df_stocks_buy = df_stocks_stocks[df_stocks_stocks['delta'].apply(lambda x: x >= DT1[0] and x <= DT1[1])].iloc[0]
            df_stocks_sell = df_stocks_stocks[df_stocks_stocks['delta'].apply(lambda x: x >= DT2[0] and x <= DT2[1])].iloc[0]

            #print(df_stocks_buy)
            # Rename the buy and sell open and close columns and get first buy and sell times
            df_stocks_buy = df_stocks_buy.rename({'open': 'buy_price', 'delta': 'delta_buy'}).loc[['buy_price', 'delta_buy']]
            df_stocks_sell = df_stocks_sell.rename({'open': 'sell_price', 'delta': 'delta_sell'}).loc[['sell_price', 'delta_sell']]

            #Combine the tweet, buy and sell prices into dataframe and store
            stock_list.append(pd.concat([df_tweet.loc[i],df_stocks_buy, df_stocks_sell]))
        except:
            pass
    if len(stock_list)==0:
        return []
    else:
        return pd.concat(stock_list, axis=1).T

snp500 = pd.read_csv('/home1/sgmark/networks/erdos_twitter_project/Data/Stock_indices/snp500_list.csv')
snp500 = snp500['Symbol'].to_list()

def aggregate_tweets_and_stocks(n):
    ticker = snp500[n]
    df_tweet_ticker = df_tweet[df_tweet['Company_ticker']==ticker]
    df_stock_ticker = df_stock[df_stock['ticker']==ticker]
    df_stock_buy_sell = aggregate_time_delayed_stock_data(df_stock_ticker, df_tweet_ticker, DT1, DT2)

    return df_stock_buy_sell

def main():
    my_list = []
    pool = mp.Pool(12)
    results = [pool.apply_async(aggregate_tweets_and_stocks, args=[k]) for k in range(51,76)]
    pool.close()
    pool.join()
    output = [p.get() for p in results]
#     with concurrent.futures.ProcessPoolExecutor() as executor:
#         results = executor.map(aggregate_tweets_and_stocks,range(51))
    for entry in output:
        if len(entry)!=0:
            my_list.append(entry)

    return pd.concat(my_list, axis=0)


t_0 = time.time()

if __name__ == "__main__":
    df = main()
    df.to_csv("merged_51_75.csv")

t_elapsed = time.time() - t_0

print(f"Elapsed time: {t_elapsed}")
