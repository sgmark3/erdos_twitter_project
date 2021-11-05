from time import sleep
from twitter_to_csv import get_twitter_data
import os
import pandas as pd

def combine_files():
    # How to build a query , check this for details 
    # https://developer.twitter.com/en/docs/twitter-api/tweets/search/integrate/build-a-query
    snp500_df = pd.read_csv("data\Stock_indices\snp500_list.csv")
    username_df = pd.read_csv("data\Stock_indices\Twitter_Users .csv")
    
    for i in range(len(snp500_df)):
        #if i < 379: continue
        ticker = snp500_df['Symbol'].iloc[i]
        name = snp500_df['Security'].iloc[i].split(' ')
        print(i, '    name=', ' '.join(name))
        outputfilename = ''.join(name)
        filename = 'df_'+outputfilename
        count1 = 0
        count2 = 0
        count3 = 0
        if filename+'.csv' in os.listdir('data\Tweets_Raw _0to10'):
            count1 += 1
        if filename+'.csv' in os.listdir('data\Tweets_Raw _10to20'):
            count2 += 1
        if filename+'.csv' in os.listdir('data\Tweets_Raw _20to34'):
            count3 += 1

        print(count1, count2, count3)
        outputfilename = filename+'.csv'
        file1 = os.path.join('data\Tweets_Raw _0to10', outputfilename)
        file2 = os.path.join('data\Tweets_Raw _10to20', outputfilename)
        file3 = os.path.join('data\Tweets_Raw _20to34', outputfilename)
        if os.path.exists(file1):
            print('\t\t First file exixts')
            df1 = pd.read_csv(file1)
            print(len(df1))
        if os.path.exists(file2):
            print('\t\t\t\t\t\t Second file exixts')
            df2 = pd.read_csv(file2)
            print(len(df2))
        if os.path.exists(file3):
            print('\t\t\t\t\t\t Third file exixts')
            df3 = pd.read_csv(file3)
            print(len(df3))
        frames = []
        if count1==1 : frames.append(df1)
        if count2==1 : frames.append(df2)
        if count3==1 : frames.append(df3)
        
        if len(frames)>0:
            print(outputfilename, 'non empty file')
            result = pd.concat(frames)    
            print(len(result))
            result.to_csv(os.path.join('data\Tweets_Raw', outputfilename), index=False)


def main():
    combine_files()


if __name__ == "__main__":
    main()