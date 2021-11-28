"""
Returns stock prices with timestamps following the creation of a tweet within a specified time window
[after,before], fed as inputs "before" and "after". This script is an implementation for a single tweet
that pertains to a single company in snp500 list.
"""


import csv
import pandas as pd
import numpy as np
import subprocess
import os

cmd = subprocess.Popen('pwd', stdout=subprocess.PIPE)
cmd_out, cmd_err = cmd.communicate()
local_path = os.fsdecode(cmd_out).strip()

#load stock price data
df_googl=pd.read_csv(local_path+"/erdos_twitter_project/data/stocks/GOOGL.csv")
df_googl['date_time']=pd.to_datetime(df_googl.time)

#load tweet data
tweets=pd.read_parquet(local_path+\
                   "/erdos_twitter_project/Data_Preprocessed/df_tweets_Shashank_features_added_part1.parquet")
tweets=pd.concat([tweets,\
                  pd.read_parquet(local_path+"/erdos_twitter_project/Data_Preprocessed/df_tweets_Shashank_features_added_part2.parquet")])

tweets=tweets[['created_at','text']]

#extract tweets that mention GOOGL
google_tweets=pd.DataFrame([item for item in tweets.values if "$GOOGL" in item[1].split()],columns=['created_at','text'])

#modify 0 to pick tweet of any index from the google_tweets dataframe
tweet_iloc=0

#modify the time in seconds to extract stock prices with time stamps in the interval [after,before]
before=50*3600
after=3600

def get_subsequent_stock_prices(df,tweet_iloc,date_and_time,before,after):
    df['delta']=[(item - pd.to_datetime(date_and_time)).total_seconds() for item in df.date_time.values]
    df=df.drop(['time','date_time'],axis=1)
    #df=df[(df['delta'] <= before) & (df['delta'] >= after)].sort_values(by=['delta'])
    df=df[df['delta'] >= after].merge(df[df['delta'] <= before]).sort_values(by=['delta'])
    time_of_creation=[(tweet_iloc,date_and_time)]
    index=pd.MultiIndex.from_product([time_of_creation,list(range(len(df.values)))],names=['iloc_and_toc','index'])
    return pd.DataFrame(df.values,index=index,columns=df.columns,dtype=float)

if __name__=="__main__":
    df = get_subsequent_stock_prices(df_googl,tweet_iloc,google_tweets.iloc[tweet_iloc]['created_at'],\
                                     before,after)
    df.to_csv(local_path+'/erdos_twitter_project/data/stocks/googl_stock_tweet.csv')
