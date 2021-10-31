#!/usr/bin/env python
# coding: utf-8

# In[364]:


import re
import csv
import pandas as pd
import bs4 as BeautifulSoup


# In[365]:


df = pd.read_csv("stock.csv")
tweets = df.text


# In[370]:


tweet_info = []
url_pattern = re.compile(r'https://[a-z0-9A-Z./]*')
hashtag_pattern = re.compile(r'#[A-Za-z0-9]*') 
for tweet in tweets:
    url_strings = url_pattern.findall(tweet) #selects and removes urls if present
    if  len(url_strings) != 0:
        for match in url_strings:
            span = re.search(match,tweet).span()
            tweet = tweet[:span[0]].strip() + tweet[span[1]:].strip()
        
    hashtag_strings = hashtag_pattern.findall(tweet) #selects and removes hashtags if present
    if len(hashtag_strings) != 0:
        for match in hashtag_strings:
            span = re.search(match,tweet).span()
            tweet = tweet[:span[0]].strip() + tweet[span[1]:].strip()
    
    d = {}
    for string in tweet.split():
        d['handles'] = re.findall(r'@[a-zA-Z0-9_]*',tweet)
        d['numbers'] = re.findall(r'[0-9]+[%]*',tweet)
        d['texts'] = re.findall(r'[a-zA-Z0-9$&@]+.',tweet)
        d['tickers'] = [ticker.strip() for ticker in re.findall(r'[$A-Z]+',tweet) 
                   if (len(ticker) == 4) or (len(ticker) == 5)]
        d['hashtags'] = hashtag_strings
    tweet_info.append(d)
    


# In[ ]:


#[" ".join([entry.strip() for entry in tweet['texts']]) for tweet in tweet_info] #cleaned tweets, uncomment to check


# In[371]:


#[item['handles'] for item in tweet_info] #handles, tickers (there is some junk in this list), hashtags can be accessed here


# In[ ]:




