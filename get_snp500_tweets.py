from time import sleep
from twitter_to_csv import get_twitter_data

import pandas as pd


def main():
    # How to build a query , check this for details 
    # https://developer.twitter.com/en/docs/twitter-api/tweets/search/integrate/build-a-query
    snp500_df = pd.read_csv("data\Stock_indices\snp500_list.csv")
    #print(snp500_df.head())
    query_file = open('query_file.txt', 'w')
    savenames = []
    for i in range(len(snp500_df)):
        #print("ticker ", snp500_df['Symbol'].iloc[i], " company ", snp500_df['Security'].iloc[i])
        if i < 202 : continue
        ticker = snp500_df['Symbol'].iloc[i]
        name = snp500_df['Security'].iloc[i].split(' ')
        name_to_use = name[0]
        ticker_to_use = "#"+ticker+" OR $"+ticker
        if len(ticker) > 2 :
            ticker_to_use += " OR "+ticker
        if len(name[0])<=3 :
            query_file.write("special case ................. \n ")
            name_to_use = ' '.join(name)
        outputfilename = ''.join(name)
        if outputfilename not in savenames:
            savenames.append(outputfilename)
        else:
            query_file.write(outputfilename+ ' POSSIBLE duplicate')
            print(outputfilename + " DUPLICATE")
        out_string = "ticker: {t} , company: {n}  \n||||||||||| query = {tick} OR ({c}) \t saveName= df_{o}.csv \n\n".format(t=ticker, tick=ticker_to_use, c=name_to_use, n=' '.join(name), o=outputfilename)
        query_file.write(out_string)
        #query = f""""#{ticker}" OR "${ticker}" """ #ticker_to_use+ " OR "+ name_to_use         # now define number of total tweets you want, should be greater than max_results_per_query
        #query = """"{}" OR "#{}" OR "${}" """.format(' '.join(name), ticker, ticker)
        query = """"{}" """.format(' '.join(name))
        number_of_tweets = 19000  # now define output file name
        filename = 'df_'+outputfilename
        print(query, number_of_tweets, filename)
        get_twitter_data(query=query, numtweets=number_of_tweets, output_file=filename)
        sleep(1)
    query_file.close()

if __name__ == "__main__":
    main()
