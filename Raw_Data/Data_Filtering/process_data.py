import pandas as pd
import os
import math 
def get_n_entries(mentions):
    #print(mentions)
    if mentions != 0 :
        return len(mentions.split(','))-1
    return 0
def get_media_value(media_type):
    if media_type != 0 :
        return 1
    return 0

def process_df(df):
    df = df.drop(columns=['name', 'profile_image_url', 'username', 'location', 'possibly_sensitive', 'tweet_id', 'author_id', 'source', 'in_reply_to_user_id'])
    df.entities_mentions = df.entities_mentions.fillna(0)
    df.entities_cashtags = df.entities_cashtags.fillna(0)
    df.entities_hashtags = df.entities_hashtags.fillna(0)
    df.entities_urls = df.entities_urls.fillna(0)
    df.media_type = df.media_type.fillna(0)

    df['entities_mentions'] = df.entities_mentions.apply(lambda x: get_n_entries(x) )
    df['entities_cashtags'] = df.entities_cashtags.apply(lambda x: get_n_entries(x) )
    df['entities_hashtags'] = df.entities_hashtags.apply(lambda x: get_n_entries(x) )
    df['entities_urls'] = df.entities_urls.apply(lambda x: get_n_entries(x) )
    df['media_type'] = df.media_type.apply(lambda x: get_media_value(x) )
    df = df.sort_values(by='created_at',ascending=False)
    df = df.drop_duplicates()
    return df

def get_dataset():
    count = 0
    input_dir = 'data\Tweets_Raw'
    output_dir = 'data\processed_v2'
    for filename in os.listdir(input_dir):
        if filename.endswith(".csv"):
            print('file = ', filename)
            df = pd.read_csv( os.path.join(input_dir, filename))
            count += len(df)
            df = process_df(df)
            df.to_csv(os.path.join(output_dir, filename), index=False)
            print('input :', os.path.join(input_dir, filename))
            print('output :', os.path.join(output_dir, filename), '\n')
    print(count)

def combine_df():
    snp500_df = pd.read_csv("data\Stock_indices\snp500_list.csv")
    #print(snp500_df.head())
    n1 = 0
    n2 = 0
    saved_dir1 = 'data\Tweets_Raw\processed_v1'
    saved_dir2 = 'data\Tweets_Raw\processed_v2'
    output_dir = 'data\Tweets_Raw'
    for i in range(len(snp500_df)):
        #if i > 5 : continue
        name = snp500_df['Security'].iloc[i].split(' ')
        outputfilename = 'df_'+''.join(name)+'.csv'
        print(outputfilename)
        file1 = os.path.join(saved_dir1, outputfilename)
        file2 = os.path.join(saved_dir2, outputfilename)
        if os.path.exists(file1):
            print('\t\t First file exixts')
            n1 += 1
        df1 = pd.read_csv(file1)
        frames = [df1]
        if os.path.exists(file2):
            print('\t\t\t\t\t\t Second file exixts')
            n2 += 1
            df2 = pd.read_csv(file2)
            frames.append(df2)

        result = pd.concat(frames)    
        result.to_csv(os.path.join(output_dir, outputfilename), index=False)

if __name__ == "__main__":
    combine_df()
