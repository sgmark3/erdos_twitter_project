
import twitter_api 
import pandas as pd
import os
from save_to_csvfile import save_to_csv
import json

# function to perform data extraction
def scrape(words, date_until, numtweet):
    search_phrase = words
    tweets = twitter_api.my_api.search_tweets(q=search_phrase, count=numtweet)
    # detailes in https://developer.twitter.com/en/docs/twitter-api/v1/data-dictionary/object-model/tweet
    out_dict = {}
    data = []
    for t in tweets:
        tmp_dict = {
                    'created_at' : t.created_at,
                    'tweet_id':t.id,
                    'text' : t.text,
                    'retweet_count' : t.retweet_count,
                    'favorite_count' : t.favorite_count,
                    'truncated' : t.truncated,
                    'username' : t.user.screen_name,
                    'followers_count' : t.user.followers_count,
                    'friends_count' : t.user.friends_count,
                    'favourites_count' : t.user.favourites_count,
                    'listed_count'   : t.user.listed_count,
                    'user_created_at' : t.user.created_at,
                    'statuses_count' : t.user.statuses_count,
                    'location' : t.user.location,
                    'hashtags' : t.entities['hashtags'],
                    'symbols'  : t.entities['symbols'],
                    'user_mentions' : t.entities['user_mentions'],
                    'source'   :  t.source,
                    'in_reply_to_user_id' : t.in_reply_to_user_id,
        }
        data.append(tmp_dict)    
    # for d in data:
    #     print("{} ".format(d).encode('cp850', errors='replace'))
    df = pd.DataFrame(data)
    print(df)
    output_file = 'out.csv'
    header_state = False  if os.path.isfile(output_file) else True
    df.to_csv(output_file , mode='a', header=header_state, index = False)


if __name__ == '__main__':
    # Enter Hashtag and initial date
    ## Enter Twitter HashTag to search for" 
    words = "stock"
    # Enter Date since The Tweets are required in yyyy-mm--dd
    date_until = "2019-01--01"
    # number of tweets you want to extract in one run
    numtweet = 5
    scrape(words, date_until, numtweet)
    #scape_to_file(words, date_until, numtweet)
    print('Scraping has completed!')