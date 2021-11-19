import pandas as pd
import datetime

def clean_and_timestamp_stocks(df_stocks):
    # This function is only for single stock data frames

    # Shorten stock column names and drop unneeded columns
    df_stocks = df_stocks.rename(columns={'1. open': 'open', '2. high': 'high', '3. low': 'low',
    '4. close': 'close', '5. volume': 'volume', 'time': 'time_stamp'})
    df_stocks = df_stocks.drop(['high', 'low', 'volume'], axis=1)

    # Drop duplicate stock price times
    df_stocks = df_amzn.drop_duplicates(subset=['time_stamp'])

    # Convert time stamps from string to date time
    df_stocks['time_stamp']=df_stocks['time_stamp'].apply(lambda x: datetime.datetime.strptime(x,
    '%Y-%m-%d %H:%M:%S'))

    return df_stocks

def remove_prices_outside_trading(df_stocks):
    # This function is for any collection of stock data

    # Filter out prices before market open
    df1 = df_stocks[df_stocks['time_stamp'].apply(lambda x: x.hour>=9 and x.minute >=30)]

    # Filter out prices after market close
    df2 = df1[df1['time_stamp'].apply(lambda x: x.hour<16)]
    return df2

def aggregate_time_delayed_stock_data(df_stocks, df_tweet, before, after):
    # This function for tweets and assets already identified to be the same company
    stock_list = []
    for i in range(len(df_tweet)):
        date_and_time = df_tweet.iloc[i]['time_stamp']
        df=df[df['delta'] >= after].merge(df[df['delta'] <= before]).sort_values(by=['delta'])
        time_of_creation=[(i,date_and_time)]
        index=pd.MultiIndex.from_product([time_of_creation,list(range(len(df.values)))],names=['iloc_and_toc','index'])
        stock_list.append(pd.DataFrame(df.values,index=index,columns=df.columns)).dropna()
    return pd.concat(stock_list)


def get_returns_and_aggregate_data:(df_stocks, df_tweets):
