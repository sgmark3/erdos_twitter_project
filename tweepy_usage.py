
import twitter_api 
import pandas as pd
import sys
from save_to_csvfile import save_to_csv
import json

# function to perform data extraction
def scrape(words, date_until, numtweet):
      
    search_phrase = words
    tweets = twitter_api.my_api.search_tweets(q=search_phrase, count=numtweet)
    # detailes in https://developer.twitter.com/en/docs/twitter-api/v1/data-dictionary/object-model/tweet
    with open("sample_tweets_.txt", "w", encoding="utf-8") as f:
        for t in tweets:
            f.write(f"""Created : {t.created_at} 
                        ID:{t.id} 
                        Text : {t.text}
                        User : {t.user}
                        retweet_count : {t.retweet_count}
                        favorite_count : {t.favorite_count}
                        truncated : {t.truncated}
                        entities  : {t.entities}
                        username : {t.user.screen_name}
                        followers_count : {t.user.followers_count}
                        friends_count : {t.user.friends_count}
                        favourites_count : {t.user.favourites_count}
                        listed_count   : {t.user.listed_count}
                        user created_at : {t.user.created_at}
                        location : {t.user.location}
                        hashtags : {t.entities['hashtags']}
                        symbols  : {t.entities['symbols']}
                        \n\n""")

def scape_to_file(words, date_until, numtweet):
    tweets = twitter_api.my_api.search_tweets(q=words, count=numtweet)
    #save_to_csv(tweets, 'stock')
    n=0
    for t in tweets:
        n += 1
        #print("{} ".format(t).encode('cp850', errors='replace'))
    print(n)
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