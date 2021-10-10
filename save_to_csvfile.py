
import pandas as pd

def unroll(data):
    tmp = {}
    for key, value in data.items():
        if key == 'public_metrics':
            for k, v in data[key].items():
                tmp[k] = v
        else:
            tmp[key] = value
    return tmp

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
    train.to_csv(output_name+'.csv')


