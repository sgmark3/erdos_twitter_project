from time import sleep
from twitter_to_csv import get_twitter_data
import os
import pandas as pd

def combine_files():
    # How to build a query , check this for details 
    # https://developer.twitter.com/en/docs/twitter-api/tweets/search/integrate/build-a-query
    snp500_df = pd.read_csv("data\\Stock_indices\\snp500_list.csv")
    username_df = pd.read_csv("data\\Stock_indices\\Twitter_Users .csv")
    
    for i in range(len(snp500_df)):
        print(i, ' th ticker ')
        ticker = snp500_df['Symbol'].iloc[i]
        name = snp500_df['Security'].iloc[i].split(' ')
        print(i, '    name=', ' '.join(name))
        outputfilename = ''.join(name)
        filename = 'df_'+outputfilename
        count1 = 0
        count2 = 0
        count3 = 0
        count4 = 0
        count5 = 0
        count6 = 0
        if filename+'.csv' in os.listdir('data\\user_company_name\\Tweets_Raw_0to10'):
            count1 += 1
        if filename+'.csv' in os.listdir('data\\user_company_name\\Tweets_Raw_10to20'):
            count2 += 1
        if filename+'.csv' in os.listdir('data\\user_company_name\\Tweets_Raw_20to34'):
            count3 += 1
        if filename+'.csv' in os.listdir('data\\user_company_name\\Tweets_Raw_34to44'):
            count4 += 1
        if filename+'.csv' in os.listdir('data\\user_company_name\\Tweets_Raw_44to54'):
            count5 += 1
        if filename+'.csv' in os.listdir('data\\user_company_name\\Tweets_Raw_54to68'):
            count6 += 1

        outputfilename = filename+'.csv'
        print(i, ticker, outputfilename)

        file1 = os.path.join('data\\user_company_name\\Tweets_Raw_0to10', outputfilename)
        file2 = os.path.join('data\\user_company_name\\Tweets_Raw_10to20', outputfilename)
        file3 = os.path.join('data\\user_company_name\\Tweets_Raw_20to34', outputfilename)
        file4 = os.path.join('data\\user_company_name\\Tweets_Raw_34to44', outputfilename)
        file5 = os.path.join('data\\user_company_name\\Tweets_Raw_44to54', outputfilename)
        file6 = os.path.join('data\\user_company_name\\Tweets_Raw_54to68', outputfilename)
        if os.path.exists(file1):
            df1 = pd.read_csv(file1)
            print('\t\t\t\t\t\t First file exixts', len(df1))
        if os.path.exists(file2):
            df2 = pd.read_csv(file2)
            print('\t\t\t\t\t\t Second file exixts', len(df2))
        if os.path.exists(file3):
            df3 = pd.read_csv(file3)
            print('\t\t\t\t\t\t third file exixts', len(df3))
        if os.path.exists(file4):
            df4 = pd.read_csv(file4)
            print('\t\t\t\t\t\t forth file exixts', len(df4))
        if os.path.exists(file5):
            df5 = pd.read_csv(file5)
            print('\t\t\t\t\t\t fifth file exixts', len(df5))
        if os.path.exists(file6):
            df6 = pd.read_csv(file6)
            print('\t\t\t\t\t\t sixth file exixts', len(df6))
        frames = []
        if count1==1 : frames.append(df1)
        if count2==1 : frames.append(df2)
        if count3==1 : frames.append(df3)        
        if count4==1 : frames.append(df4)
        if count5==1 : frames.append(df5)
        if count6==1 : frames.append(df6)
        
        if len(frames)>0:
            print(outputfilename, 'non empty file')
            result = pd.concat(frames)    
            print('final lenght ', len(result))
            result.to_csv(os.path.join('data\Tweets_Raw', outputfilename), index=False)


def main():
    combine_files()


if __name__ == "__main__":
    main()