"""
This set up gives full-archive Tweet search 
"""
import requests
from twitter_daq.twitter_api import bearer_oauth
from twitter_daq.save_to_csvfile import save_to_csv
import os
import json
import pandas as pd


search_url = "https://api.twitter.com/2/tweets/search/all"
max_results_per_query = 10
# check the following for details
#  https://developer.twitter.com/en/docs/twitter-api/tweets/search/api-reference/get-tweets-search-all


def get_fullarchive_tweets(query='', start_date='2019-01-01T00:00:00Z', next_token=None, filename='stock'):
    """
    This function takes in a search term query and creates a csv file with json response from twitter
    """
    query_params = {'query': query+' lang:en', 
                    'tweet.fields': 'attachments,author_id,created_at,entities,geo,id,in_reply_to_user_id,public_metrics,possibly_sensitive,referenced_tweets,source,text,withheld',
                    'expansions' :'attachments.media_keys,author_id,in_reply_to_user_id,entities.mentions.username,referenced_tweets.id,referenced_tweets.id.author_id', 
                    'user.fields':'created_at,entities,id,location,name,pinned_tweet_id,profile_image_url,public_metrics,url,username,withheld', 
                    'media.fields' : 'duration_ms,height,media_key,type,url,width,public_metrics,alt_text',
                    'max_results' : max_results_per_query,
                    'start_time': start_date
                     }
    if next_token is not None:
        query_params['next_token'] = next_token 

    response = requests.get(search_url, auth=bearer_oauth, params=query_params)
    print(response.status_code)
    if response.status_code != 200:
        raise Exception(response.status_code, response.text)
    json_response = response.json()
    with open(query+'.json', 'w', encoding="utf-8") as outfile:
        json.dump(json_response, outfile, indent=4, sort_keys=True)
    save_to_csv(json_response, filename)
    return json_response["meta"]

def get_twitter_data(query='', numtweets=10, output_file=''):
    next_token = None
    # for n in range(int(numtweets/max_results_per_query)):
    #     if os.path.isfile(output_file):
    #         data = pd.read_csv(output_file+'.csv')
    #         last_tweet_id = data.id.iloc[-1] -1 
    #         print(last_tweet_id + 1)
    #     get_fullarchive_tweets(query=query, filename=output_file)
    output = get_fullarchive_tweets(query=query, next_token=next_token, filename=output_file)
    print(output)

def main():
    # Optional params: start_time,end_time,since_id,until_id,max_results,next_token,
    # expansions,tweet.fields,media.fields,poll.fields,place.fields,user.fields
    # https://developer.twitter.com/en/docs/twitter-api/tweets/search/api-reference/get-tweets-search-all

    # https://developer.twitter.com/en/docs/twitter-api/enterprise/engagement-api/overview
    # https://github.com/twitterdev/Gnip-Insights-Interface/blob/master/tweet_engagements.py
    query = 'snp500'
    get_twitter_data(query=query, numtweets=10, output_file=query)


if __name__ == "__main__":
    main()