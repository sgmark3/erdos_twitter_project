
import requests
import json
import pandas as pd
from Twitter_data_get.save_to_csvfile import flatten_dict, unfold_dict
import os.path as os_path
from datetime import datetime
import streamlit as st

search_url = "https://api.twitter.com/2/tweets"
# check the following for details
#  https://developer.twitter.com/en/docs/twitter-api/tweets/lookup/api-reference/get-tweets
fmt = '%Y-%m-%dT%H:%M:%S.000Z'

def bearer_oauth(r):
    """
    Method required by bearer token authentication.
    """
    r.headers["Authorization"] = "Bearer "+st.secrets["BEARER_TOKEN"]
    r.headers["User-Agent"] = st.secrets["User-Agent"]
    return r

def connect_to_endpoint(url, params):
    response = requests.get(url, auth=bearer_oauth, params=params)
    print(response.status_code)
    if response.status_code != 200:
        raise Exception(response.status_code, response.text)
    return response.json()

def json_to_csv(data, output_name=None):
    if 'data' not in data: return
    tweet_data = data['data']              # this is tweet data
    user_data  = data['includes']['users'] # this is user data
    if 'media' in data['includes']:
        media_data = data['includes']['media'] # this is media data
    else:
        media_data = {}
    # first get flattened dictionary
    tweet_data_unfolded = []
    for data in tweet_data:
        tweet_data_unfolded.append(flatten_dict(data))

    # now get flatenned user dictionary
    user_unfolded = []
    for data in user_data:
        user_unfolded.append(flatten_dict(data))
    
    media_unfoldeded = []
    for data in media_data:
        media_unfoldeded.append(flatten_dict(data))

    tweet_df = pd.DataFrame.from_dict(tweet_data_unfolded)
    tweet_df.rename(columns={"id": "tweet_id"}, inplace=True)
    tweet_df.rename(columns={"attachments_media_keys": "media_key"}, inplace=True)
    if "media_key" in tweet_df:
        tweet_df["media_key"] = tweet_df["media_key"].apply(lambda x: str(x[0]) if isinstance(x, list) else ' ' )

    user_df = pd.DataFrame.from_dict(user_unfolded)
    user_df.rename(columns={"id": "author_id"}, inplace=True)
    media_df = pd.DataFrame.from_dict(media_unfoldeded)
    if "media_key" in media_df:
        media_df["media_key"] = media_df["media_key"].apply(lambda x: str(x) )
        media_df.rename(columns={"type": "media_type"}, inplace=True)


    ## now merge tweets with corresponding user parameters
    result_df = tweet_df.merge(user_df, how='left', on='author_id', suffixes=('', '_user'))
    if  "media_key" in media_df:
        result_df = result_df.merge(media_df, how='left', on='media_key', suffixes=('', '_media'))
    for col in ['created_at', 'created_at_user']:
        result_df[col] = result_df[col].apply(lambda x: datetime.strptime(x, fmt) ) 
        result_df[col] = result_df[col].dt.tz_localize('UTC')
        result_df[col] = result_df[col].dt.tz_convert('US/Eastern').dt.tz_localize(None)


    columns_to_add = ['author_id', 'created_at',
       'entities_cashtags', 'entities_hashtags', 'entities_urls', 'tweet_id',
       'possibly_sensitive', 'public_metrics_like_count',
       'public_metrics_quote_count', 'public_metrics_reply_count',
       'public_metrics_retweet_count', 'source', 'text',
       'entities_mentions', 'in_reply_to_user_id',
       'created_at_user', 'location', 'name',
       'profile_image_url', 'public_metrics_followers_count',
       'public_metrics_following_count', 'public_metrics_listed_count',
       'public_metrics_tweet_count', 'username', 'media_type']
    # columns not included : 'media_key', referenced_tweets, entities_annotations,'entities_url_urls',
    #'pinned_tweet_id', 'entities_description_urls',
    #'entities_description_hashtags', 'entities_description_cashtags',
    #'entities_description_mentions'
    final_df = pd.DataFrame(columns=columns_to_add)
    for col in columns_to_add:
        if col in result_df:
            final_df[col] = result_df[col]
    final_df.entities_hashtags = final_df.entities_hashtags.apply(lambda x: unfold_dict(x, 'tag') )
    final_df.entities_cashtags = final_df.entities_cashtags.apply(lambda x: unfold_dict(x, 'tag') )
    final_df.entities_urls = final_df.entities_urls.apply(lambda x: unfold_dict(x, 'display_url') )
    final_df.entities_mentions = final_df.entities_mentions.apply(lambda x: unfold_dict(x, 'username') )

    ## 
    return final_df
        
        
def get_info(tweet_url):
    input_tweet_id = tweet_url.strip().split('/')[-1]
    query_params = {'ids' : str(input_tweet_id),
                    'tweet.fields': 'attachments,author_id,created_at,entities,id,in_reply_to_user_id,public_metrics,possibly_sensitive,referenced_tweets,source,text,withheld',
                    'expansions' :'attachments.media_keys,author_id,in_reply_to_user_id,entities.mentions.username,referenced_tweets.id,referenced_tweets.id.author_id', 
                    'user.fields':'created_at,id,location,entities,name,pinned_tweet_id,profile_image_url,public_metrics,url,username,withheld', 
                    'media.fields' : 'duration_ms,height,media_key,type,url,width,public_metrics,alt_text',
                    } 
    # json_response = connect_to_endpoint(search_url, query_params)
    # print(json.dumps(json_response, indent=4, sort_keys=True))
    # with open('finance.json', 'w', encoding="utf-8") as outfile:
    #     json.dump(json_response, outfile, indent=4, sort_keys=True)


    json_response = connect_to_endpoint(search_url, params=query_params)
    #print(json.dumps(json_response, indent=4, sort_keys=True))
    tweet_df = json_to_csv(json_response, 'input')
    return tweet_df
    
    
def main():
    # Optional params: start_time,end_time,since_id,until_id,max_results,next_token,
    # expansions,tweet.fields,media.fields,poll.fields,place.fields,user.fields
    #input_url = str(input("Enter tweets link here :"))
    input_url = 'https://twitter.com/markets/status/1458402478123327497'
    input_tweet_id = input_url.strip().split('/')[-1]
    query_params = {'ids' : str(input_tweet_id),
                    'tweet.fields': 'attachments,author_id,created_at,entities,id,in_reply_to_user_id,public_metrics,possibly_sensitive,referenced_tweets,source,text,withheld',
                    'expansions' :'attachments.media_keys,author_id,in_reply_to_user_id,entities.mentions.username,referenced_tweets.id,referenced_tweets.id.author_id', 
                    'user.fields':'created_at,id,location,entities,name,pinned_tweet_id,profile_image_url,public_metrics,url,username,withheld', 
                    'media.fields' : 'duration_ms,height,media_key,type,url,width,public_metrics,alt_text',
                    } 
    # json_response = connect_to_endpoint(search_url, query_params)
    # print(json.dumps(json_response, indent=4, sort_keys=True))
    # with open('finance.json', 'w', encoding="utf-8") as outfile:
    #     json.dump(json_response, outfile, indent=4, sort_keys=True)


    json_response = connect_to_endpoint(search_url, params=query_params)
    #print(json.dumps(json_response, indent=4, sort_keys=True))
    tweet_df = json_to_csv(json_response, 'input')
    print(tweet_df)

if __name__ == "__main__":
    main()
