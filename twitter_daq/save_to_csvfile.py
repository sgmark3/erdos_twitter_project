
import pandas as pd
import json
import os.path as os_path


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
    tweet_data = data['data']              # this is tweet data
    user_data  = data['includes']['users'] # this is user data

    # first get flattened dictionary
    tweet_data_unfolded = []
    for data in tweet_data:
        tweet_data_unfolded.append(flatten_dict(data))

    # now get flatenned user dictionary
    user_unfolded = []
    for data in user_data:
        user_unfolded.append(flatten_dict(data))
    
    tweet_df = pd.DataFrame.from_dict(tweet_data_unfolded)
    tweet_df.rename(columns={"id": "tweet_id"}, inplace=True)
    user_df = pd.DataFrame.from_dict(user_unfolded)
    user_df.rename(columns={"id": "author_id"}, inplace=True)
    
    ## now if any columns contain dictionaries, unfold it using unfold_dict
    ## think of better way to implement to include edge cases.
    # tweet_df.entities_hashtags = tweet_df.entities_hashtags.apply(lambda x: unfold_dict(x, 'tag') )
    # tweet_df.entities_urls = tweet_df.entities_urls.apply(lambda x: unfold_dict(x, 'display_url') )
    # user_df.entities_description_hashtags = user_df.entities_description_hashtags.apply(lambda x: unfold_dict(x, 'tag') )

    # now merge tweets with corresponding user parameters
    result_df = tweet_df.merge(user_df, how='left', on='author_id', suffixes=('', '_user'))

    # list any columns you want to remove
    column_to_remove = [
        'attachments_media_keys',  'possibly_sensitive','entities_mentions', 'referenced_tweets', 'entities_hashtags' , 'entities_urls' , 'entities_description_hashtags',
        'entities_annotations',  'profile_image_url', 'url', 'pinned_tweet_id', 'entities_cashtags', 'in_reply_to_user_id',
        'entities_url_urls', 'entities_description_mentions', 'entities_description_urls', 'entities_description_cashtags']
    for col_to_rm in column_to_remove:
        if col_to_rm in result_df.columns:
            result_df.drop([col_to_rm] , axis=1, inplace=True)

    # sort the columns, this makes appending data to the same file easier to handle. May need more debugging
    result_df.sort_index(axis=1, inplace=True)


    ## now finally lets save to a csv file
    if output_name is None:
        output_name = 'out'
    if os_path.isfile('data/'+output_name+'.csv'):
        result_df.to_csv('data/'+output_name+'.csv', mode='a', header=False, index=False)
    else:
        result_df.to_csv('data/'+output_name+'.csv', index=False)


if __name__ == "__main__":
    ## for testing, input a json file with response from twitter api
    with open('snp500.json', "r") as infile:
        data = json.load(infile)
    json_to_csv(data)