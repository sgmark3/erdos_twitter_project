
import twitter_api 
import pandas as pd
import os
from save_to_csvfile import save_to_csv

output_file = 'tweets_data.csv'

def unfold_dict(inputList=[] , parameter=None):
    '''
    This function takes in a list of dictionaries and returns 
    keys in that dictionary matching 'parameter'
    '''
    out_string = ''
    for entities in inputList:
        if parameter in entities:
            out_string +=  entities[parameter] + ', '
    return out_string


# function to perform data extraction
def get_tweets(words, date_until, numtweet, last_tweet_id=None):
    '''
    This function takes in a word or phrase for query and returns number of tweets = numtweet
    with 'words' in it
    This is a problem : 
    the search index has a 7-day limit. In other words, no tweets will be found for a date older than one week.

    '''
    search_phrase = words
    if not last_tweet_id:
        tweets = twitter_api.my_api.search_tweets(q=search_phrase, count=numtweet)
    else:
        tweets = twitter_api.my_api.search_tweets(q=search_phrase, count=numtweet, max_id=last_tweet_id)
    # detailes in https://developer.twitter.com/en/docs/twitter-api/v1/data-dictionary/object-model/tweet
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
                    'hashtags' : unfold_dict(t.entities['hashtags'], 'text'),
                    'symbols'  : unfold_dict( t.entities['symbols'], 'text'),
                    'mentioned_user_names' : unfold_dict(t.entities['user_mentions'], 'screen_name'),
                    'mentioned_user_ids' : unfold_dict(t.entities['user_mentions'],  'id_str'),
                    'source'   :  t.source,
                    'in_reply_to_user_id' : t.in_reply_to_user_id,
        }
        data.append(tmp_dict)    
    # for d in data:
    #     print("{} ".format(d).encode('cp850', errors='replace'))   ##### IMP incase you have encoding issue in python, use this format
    df = pd.DataFrame(data)
    #print(df)
    header_state = False  if os.path.isfile(output_file) else True
    df.to_csv(output_file , mode='a', header=header_state, index = False)

def get_twitter_data(words, date_until, numtweets):
    last_tweet_id = None
    for n in range(int(numtweets/100)):
        if os.path.isfile(output_file):
            data = pd.read_csv(output_file)
            last_tweet_id = data.tweet_id.iloc[-1] -1 
            print(last_tweet_id + 1)
        get_tweets(words, date_until, 100, last_tweet_id=last_tweet_id)


if __name__ == '__main__':
    # Enter Hashtag and initial date
    ## Enter Twitter HashTag to search for" 
    words = "stock"
    # Enter Date since The Tweets are required in yyyy-mm--dd
    date_until = "2019-01--01"
    # number of tweets you want to extract in one run
    numtweets = 10000
    #get_tweets(words, date_until, numtweet)
    get_twitter_data(words, date_until, numtweets)
    print('Scraping has completed!')