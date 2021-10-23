from twitter_to_csv import get_twitter_data

import pandas as pd


def main():

    snp500_df = pd.read_csv("data\Stock_indices\snp500_list.csv")
    #print(snp500_df.head())
    # for i in range(len(snp500_df)):
    # 	print("ticker ", snp500_df['Symbol'].iloc[i], " company ", snp500_df['Security'].iloc[i])
    query = 'aapl OR Apple'         # now define number of total tweets you want, should be greater than max_results_per_query
    number_of_tweets = 500  # now define output file name
    filename = 'df_'+query
    print(query, number_of_tweets, filename)
    get_twitter_data(query=query, numtweets=number_of_tweets, output_file=filename)


if __name__ == "__main__":
    main()
