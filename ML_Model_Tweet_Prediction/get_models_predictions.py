import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import time

import os
from sklearn.model_selection import train_test_split
from logistic_reg import get_LR
from naive_bayes import get_NaiveBayes, get_MultinomialNB
from sklearn.preprocessing import StandardScaler

# cmd = subprocess.Popen('pwd', stdout=subprocess.PIPE)
# cmd_out, cmd_err = cmd.communicate()
local_path = os.getcwd()
print(local_path)

file_location = 'data\Data_Preprocessed'
    
df=pd.read_parquet(os.path.join(local_path, file_location, "df_tweets_Shashank_features_added_part1.parquet"))
df=pd.concat([df,pd.read_parquet(os.path.join(local_path, file_location, "df_tweets_Shashank_features_added_part2.parquet")) ])

df2 = df.copy(deep=True)
# print(df2.columns)

# parameters_to_keep = ['entities_cashtags','entities_urls','public_metrics_followers_count',
#                     'public_metrics_following_count', 'public_metrics_listed_count','public_metrics_tweet_count',
#                     'Tweet_Length_characters', 'Compound_vader','Positive_vader', 'Negative_vader', 'Neutral_vader']
parameters_to_keep = ['entities_hashtags', 'entities_cashtags','entities_urls','public_metrics_followers_count',
                    'public_metrics_following_count', 'public_metrics_listed_count','public_metrics_tweet_count','media_type','entities_mentions',
                    'Word_count_Henry08_pos', 'Word_count_Henry08_neg',
                    'Word_count_LM11_pos', 'Word_count_LM11_neg',
                    'Word_count_Hagenau13_pos', 'Word_count_Hagenau13_neg',
                    'Tweet_Length_characters', 'Compound_vader','Positive_vader', 'Negative_vader', 'Neutral_vader']

dropthese=['created_at','created_at_user','text','Company_name','media_type']
for col in df2.columns:
    if col not in parameters_to_keep:
        df2=df2.drop(col,axis=1)


print(df2.columns)
y_likes = df["public_metrics_like_count"].apply(lambda x: 1 if x > 20  else 0 )
     
y_retweets= df["public_metrics_retweet_count"].apply(lambda x: 1 if x > 20  else 0 )

X = df2   
# X = df.drop(['public_metrics_like_count'],axis=1)

print(f'fraction of tweets more than 20 likes and those less than 20 likes: {sum(y_likes)/len(y_likes)} , {1-(sum(y_likes)/len(y_likes))}')
print(f'fraction of tweets more than 20 Retweets and those less than 20 Retweets: {sum(y_retweets)/len(y_retweets)} , {1-(sum(y_retweets)/len(y_retweets))}')





X_train, X_test, y_train, y_test = train_test_split(X, y_likes,
                                                    test_size = .2,
                                                    random_state=123,
                                                    shuffle=True,
                                                    stratify=y_likes)

sc = StandardScaler()
X_train = sc.fit_transform(X_train)
X_test = sc.fit_transform(X_test)

y_test  = y_test.values.reshape(-1, 1)
y_train = y_train.values.reshape(-1, 1)
    
start_1 = time.perf_counter()
get_LR(X_train, X_test, y_train, y_test)
finish_1 = time.perf_counter()
print(f'time taken : {finish_1-start_1}s')


start_2 = time.perf_counter()
get_NaiveBayes(X_train, X_test, y_train, y_test)
finish_2 = time.perf_counter()
print(f'time taken : {finish_2-start_2}s')


get_MultinomialNB(X_train, X_test, y_train, y_test)
