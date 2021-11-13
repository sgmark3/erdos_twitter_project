
from typing import final
import pandas as pd
import json
import os.path as os_path
from datetime import datetime

fmt = '%Y-%m-%dT%H:%M:%S.000Z'

def unroll(data):
    """
    unroll nested dictionary into one flattened dictionary
    This function is basic.
    """
    tmp = {}
    for key, value in data.items():
        if key == 'public_metrics':
            for k, v in data[key].items():
                tmp[k] = v
        else:
            tmp[key] = value
    return tmp


def flatten_dict(dd, separator ='_', prefix =''):
    '''
    This function takes in a nested dictionary and returns 
    a fattened dictionary'
    '''
    return { prefix + separator + k if prefix else k : v
             for kk, vv in dd.items()
             for k, v in flatten_dict(vv, separator, kk).items()
             } if isinstance(dd, dict) else { prefix : dd }

def unfold_dict(inputList=[] , parameter=None):
    '''
    This function takes in a list of dictionaries and returns 
    keys in that dictionary matching 'parameter'
    '''
    if not isinstance(inputList, list): return ''
    out_string = ''
    for entities in inputList:
        if parameter in entities:
            out_string +=  entities[parameter] + ', '
    return out_string
    
def save_to_csv(data, output_name=None):
    '''
    This function takes in a json 'data' and output_name
    and saves tweet, user parameters into output_name.csv
    json_to_csv() is the improved version
    '''
    if 'data' not in data: return
    tweet_data = data['data']
    user_data  = data['includes']['users']

    tweet_data_unfolded = []
    for data in tweet_data:
        tweet_data_unfolded.append(unroll(data))

    user_unfolded = []
    for data in user_data:
        user_unfolded.append(unroll(data))

    combined_list = []
    for data in tweet_data_unfolded:
        for user in user_unfolded:
            if data['author_id'] == user['id']:
                d5 = {**data, **user}
                combined_list.append(d5)


    train = pd.DataFrame.from_dict(combined_list)
    if output_name is None:
        output_name = 'out'
    train.to_csv('data/'+output_name+'.csv')


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

    # tweet_df.to_csv('data/Tweets_Raw/tweet_df.csv', index=False)
    # user_df.to_csv('data/Tweets_Raw/user_df.csv', index=False)
    # media_df.to_csv('data/Tweets_Raw/media_df.csv', index=False)

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

    ## now finally lets save to a csv file
    if output_name is None:
        output_name = 'out'
    if os_path.isfile('data/Tweets_Raw/'+output_name+'.csv'):
        final_df.to_csv('data/Tweets_Raw/'+output_name+'.csv', mode='a', header=False, index=False)
    else:
        final_df.to_csv('data/Tweets_Raw/'+output_name+'.csv', index=False)


if __name__ == "__main__":
    ## for testing, input a json file with response from twitter api
    with open('sample.json', "r") as infile:
        data = json.load(infile)
    json_to_csv(data)
