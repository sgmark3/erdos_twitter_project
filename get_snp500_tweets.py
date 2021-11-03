from time import sleep
from twitter_to_csv import get_twitter_data
import os
import pandas as pd
new_list=['AAPL', 'MSFT', 'AMZN']

def main():
    # How to build a query , check this for details 
    # https://developer.twitter.com/en/docs/twitter-api/tweets/search/integrate/build-a-query
    snp500_df = pd.read_csv("data\Stock_indices\snp500_list.csv")
    username_df = pd.read_csv("data\Stock_indices\Twitter_Users .csv")
    
    for i in range(len(snp500_df)):
        #if i > 10: continue
        ticker = snp500_df['Symbol'].iloc[i]
        name = snp500_df['Security'].iloc[i].split(' ')
        #if ticker not in new_list: continue
        name_to_use = name[0]
        ticker_to_use = "#"+ticker+" OR $"+ticker
        if len(ticker) > 2 :
            ticker_to_use += " OR "+ticker
        if len(name[0])<=3 :
            name_to_use = ' '.join(name)
        outputfilename = ''.join(name)
        user_name = list( username_df['Username'] )   # specify twitter user name
        user_name = [ 'from:'+x for x in user_name ][:10]
        user_name = ' OR '.join(user_name)
        #query = """"{}" ("#{}" OR "${}") """.format(' '.join(name), ticker, ticker)      # quesry for company_name AND (tags)
        #query = """"{}" """.format(' '.join(name))                   # quesry for company_name 
        query = """"{}" ({}) """.format(' '.join(name), user_name)                   # quesry for company_name , from user user_name
        number_of_tweets = 1000  # now define output file name
        filename = 'df_'+outputfilename
        #print(len(query))
        print(i, " query : ", query, '\t\t', number_of_tweets, filename)
        get_twitter_data(query=query, numtweets=number_of_tweets, output_file=filename)
        sleep(1)



if __name__ == "__main__":
    main()
