
import requests
import json
from twitter_daq.twitter_api import bearer_oauth
from twitter_daq.save_to_csvfile import json_to_csv

search_url = "https://api.twitter.com/2/tweets"
# check the following for details
#  https://developer.twitter.com/en/docs/twitter-api/tweets/lookup/api-reference/get-tweets

def connect_to_endpoint(url, params):
    response = requests.get(url, auth=bearer_oauth, params=params)
    print(response.status_code)
    if response.status_code != 200:
        raise Exception(response.status_code, response.text)
    return response.json()


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
    json_to_csv(json_response, 'input')


if __name__ == "__main__":
    main()