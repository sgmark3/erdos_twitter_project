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

def aggregate_time_delayed_stock_data(df_stock, df_tweet, DT1, DT2):
    # This function for tweets and assets already identified to be the same company
    stock_list = []
    df_stocks= df_stock.copy().sort_values(by=['time_stamp'])

    for i in df_tweet.index:
        # Get the time associated with an individual tweet
        date_and_time = df_tweet.loc[i]['time_stamp']
        #df_stocks = df_stocks[df_stocks['time_stamp']>= date_and_time]
        df_stocks['delta']= df_stocks['time_stamp'].apply(lambda x: (x-date_and_time).total_seconds())
        try:
            # Get prices that lie within buying and selling time differential
            df_stocks_buy = df_stocks[df_stocks['delta'].apply(lambda x: x >= DT1[0] and x <= DT1[1])].iloc[0]
            df_stocks_sell = df_stocks[df_stocks['delta'].apply(lambda x: x >= DT2[0] and x <= DT2[1])].iloc[0]

            #print(df_stocks_buy)
            # Rename the buy and sell open and close columns and get first buy and sell times
            df_stocks_buy = df_stocks_buy.rename({'open': 'buy_price', 'delta': 'delta_buy'}).loc[['buy_price', 'delta_buy']]
            df_stocks_sell = df_stocks_sell.rename({'open': 'sell_price', 'delta': 'delta_sell'}).loc[['sell_price', 'delta_sell']]

            #Combine the tweet, buy and sell prices into dataframe and store
            stock_list.append(pd.concat([df_tweet.loc[i],df_stocks_buy, df_stocks_sell]))
        except:
            pass 
        if len(stock_list)==0:
            return pass
        else:
            return pd.concat(stock_list, axis=1).T

def aggregate_tweets_and_stocks(snp500list, df_tweets, df_stocks, DT1, DT2):
    snp500 = pd.read_csv(snp500list)
    snp500 = snp500['Symbol'].to_list()

    my_list = []

    for ticker in snp500:
        df_tweet_ticker = df_tweets[df_tweets['Company_name']==ticker]
        df_stock_ticker = df_stocks[df_stocks['Company_name']==ticker]
        df_stock_buy_sell = aggregate_time_delayed_stock_data(df_stock_ticker, df_tweet_ticker, DT1, DT2)
        my_list.append(df_stock_buy_sell)
    return pd.concat(my_list, axis=1)
