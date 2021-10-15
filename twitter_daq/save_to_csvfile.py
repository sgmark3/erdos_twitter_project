
import pandas as pd
import json

def unroll(data):
    tmp = {}
    for key, value in data.items():
        if key == 'public_metrics':
            for k, v in data[key].items():
                tmp[k] = v
        else:
            tmp[key] = value
    return tmp

def unroll_v2(data):
    tmp = {}
    for key, value in data.items():
        if isinstance(data[key], list):
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
    out_string = ''
    for entities in inputList:
        if parameter in entities:
            out_string +=  entities[parameter] + ', '
    return out_string
    
def save_to_csv(data, output_name=None):
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
    tweet_data = data['data']
    user_data  = data['includes']['users']
    # media_data = data['includes']['media']

    tweet_data_unfolded = []
    for data in tweet_data:
        tweet_data_unfolded.append(flatten_dict(data))

    user_unfolded = []
    for data in user_data:
        user_unfolded.append(flatten_dict(data))
    
    # media_unfolded = []
    # for data in media_data:
    #     media_unfolded.append(flatten_dict(data))

    tweet_df = pd.DataFrame.from_dict(tweet_data_unfolded)
    tweet_df.rename(columns={"id": "tweet_id"}, inplace=True)
    user_df = pd.DataFrame.from_dict(user_unfolded)
    user_df.rename(columns={"id": "author_id"}, inplace=True)
    # media_df = pd.DataFrame.from_dict(media_unfolded)
    
    tweet_df.drop(['possibly_sensitive'], axis=1, inplace=True)
    tweet_df.to_csv('data/'+'tweet_df.csv')
    user_df.to_csv('data/'+'user_df.csv')
    # media_df.to_csv('data/media_df.csv')
    
    result_df = tweet_df.merge(user_df, how='left', on='author_id')
    result_df = tweet_df.merge(user_df, how='left', on='author_id')
    result_df.to_csv('data/'+'result_df.csv')
    # combined_list = []
    # for data in tweet_data_unfolded:
    #     for user in user_unfolded:
    #         if data['author_id'] == user['id']:
    #             d5 = {**data, **user}
    #             combined_list.append(d5) 

    # for data in tweet_data_unfolded:
    #     if 'attachments' not in data: continue
    #     for media in media_unfolded:
    #         if data["attachments"]["media_keys"][0] == media['media_key']:
    #             tmpdict = {**data, **media}
    #             combined_list.append(tmpdict)
    # # for d in combined_list:
    # #     print("{} ".format(d).encode('cp850', errors='replace'))  
    # final_df = pd.DataFrame.from_dict(combined_list)
    # final_df.drop(['attachments_media_keys'], axis=1, inplace=True)
    # if output_name is None:
    #     output_name = 'out'
    # final_df.to_csv('jsontocsv.csv')



if __name__ == "__main__":
    with open('snp500.json', "r") as infile:
        data = json.load(infile)
    #print(json.dumps(data, indent=4, sort_keys=True)) 
    json_to_csv(data)