"""
This set up gives full-archive Tweet search 
"""
import requests
from twitter_daq.twitter_api import bearer_oauth
from twitter_daq.save_to_csvfile import json_to_csv
from time import sleep
import json

search_url = "https://api.twitter.com/2/tweets/search/all"
max_results_per_query = 100  # maximum requests per query, minimum is 10, maximum is 500
# check the following for details
#  https://developer.twitter.com/en/docs/twitter-api/tweets/search/api-reference/get-tweets-search-all


def get_fullarchive_tweets(query='', end_date='2021-01-01T00:00:00Z', next_token=None, filename='stock'):
    """
    This function takes in a search term query and creates a csv file with json response from twitter
    """
    # Details on query can be found here
    # https://developer.twitter.com/en/docs/twitter-api/tweets/search/integrate/build-a-query
    query_params = {'query': query+' lang:en -RT', 
                    'tweet.fields': 'attachments,author_id,created_at,entities,id,in_reply_to_user_id,public_metrics,possibly_sensitive,referenced_tweets,source,text,withheld',
                    'expansions' :'attachments.media_keys,author_id,in_reply_to_user_id,entities.mentions.username,referenced_tweets.id,referenced_tweets.id.author_id', 
                    'user.fields':'created_at,id,location,entities,name,pinned_tweet_id,profile_image_url,public_metrics,url,username,withheld', 
                    'media.fields' : 'duration_ms,height,media_key,type,url,width,public_metrics,alt_text',
                    'max_results' : max_results_per_query,
                    'end_time' : end_date
                     }                    

    if next_token is not None:
        query_params['next_token'] = next_token 

    response = requests.get(search_url, auth=bearer_oauth, params=query_params)
    print(response.status_code)
    if response.status_code != 200:
        raise Exception(response.status_code, response.text)
    json_response = response.json()
    with open('sample.json', 'w') as f:
        json.dump(json_response, f, sort_keys = True, indent = 4)
    json_to_csv(json_response, filename)
    return json_response["meta"]

def get_twitter_data(query='', numtweets=500, output_file=''):
    next_token = None
    for n in range(int(numtweets/max_results_per_query)):
        output = get_fullarchive_tweets(query=query, next_token=next_token, filename=output_file )
        print(output)
        next_token = output['next_token']
        sleep(1)  # sleeps for 1 second, or else it throws error - 'Too many requests'

def main():
    # Optional params: start_time,end_time,since_id,until_id,max_results,next_token,
    # expansions,tweet.fields,media.fields,poll.fields,place.fields,user.fields
    # https://developer.twitter.com/en/docs/twitter-api/tweets/search/api-reference/get-tweets-search-all

    # first define what you want to search, if you have multiple wors, use OR, AND to concatenate
    # https://developer.twitter.com/en/docs/twitter-api/tweets/search/integrate/build-a-query
    query = 'aapl'
    # now define number of total tweets you want, should be greater than max_results_per_query
    number_of_tweets = 30
    # now define output file name
    filename = 'df_'+query
    get_twitter_data(query=query, numtweets=number_of_tweets, output_file=filename)


if __name__ == "__main__":
    main()