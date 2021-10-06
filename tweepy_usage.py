
import twitter_api 
import pandas as pd
import sys

# Set up words to track  
keywords_to_track = ['#javascript','#python']


# function to display data of each tweet
def printtweetdata(n, ith_tweet):
    print()
    print(f"Tweet {n}:")
    print(f"Username:{ith_tweet[0]}")
    print(f"Description:{ith_tweet[1]}")
    print(f"Location:{ith_tweet[2]}")
    print(f"Following Count:{ith_tweet[3]}")
    print(f"Follower Count:{ith_tweet[4]}")
    print(f"Total Tweets:{ith_tweet[5]}")
    print(f"Retweet Count:{ith_tweet[6]}")
    print(f"Tweet Text:{ith_tweet[7]}")
    print(f"Hashtags Used:{ith_tweet[8]}")


# function to perform data extraction
def scrape(words, date_until, numtweet):
      
    search_phrase = words
    tweets = twitter_api.my_api.search_tweets(q=search_phrase, count=numtweet)
    # detailes in https://developer.twitter.com/en/docs/twitter-api/v1/data-dictionary/object-model/tweet
    with open("sample_tweets_with_"+search_phrase+".txt", "w", encoding="utf-8") as f:
        for t in tweets:
            print("Found id :" , t.id)
            f.write(f"""Created : {t.created_at} 
                        ID:{t.id} 
                        Text : {t.text}
                        User : {t.user}
                        retweet_count : {t.retweet_count}
                        favorite_count : {t.favorite_count}
                        \n\n""")


  
if __name__ == '__main__':
      

    # Enter Hashtag and initial date
    ## Enter Twitter HashTag to search for" 
    words = "python"
    
    # Enter Date since The Tweets are required in yyyy-mm--dd
    date_until = "2019-01--01"
      
    # number of tweets you want to extract in one run
    numtweet = 100
    scrape(words, date_until, numtweet)
    print('Scraping has completed!')