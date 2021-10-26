#!/usr/bin/env python
# coding: utf-8

# In[17]:


import numpy as np
import os
import requests
from ediblepickle import pickle
from bs4 import BeautifulSoup
import pandas as pd
import csv
import sys
import subprocess
from urllib.parse import quote
from retrying import retry
from time import sleep
from ediblepickle import checkpoint


# In[ ]:

# set the local path

cmd = subprocess.Popen('pwd', stdout=subprocess.PIPE)
cmd_out, cmd_err = cmd.communicate()
local_path = os.fsdecode(cmd_out).strip()


# In[8]:

# run the following command on your terminal in the beginning before running this script:
# export API_key="your api_key goes here"

API_key=os.getenv('API_key')

cache_dir = 'cache'
if not os.path.exists(cache_dir):
    os.mkdir(cache_dir)

@checkpoint(key=lambda args, kwargs: quote(args[0]+'_'+args[1]) + '.pkl', work_dir=cache_dir)
@retry
def load_data(symbol,month):
    CSV_URL = 'https://www.alphavantage.co/query?function=TIME_SERIES_INTRADAY_EXTENDED&symbol='+    symbol + '&interval=1min&slice='+    month+'&apikey='+API_key
    with requests.Session() as s:
        download = s.get(CSV_URL)
        decoded_content = download.content.decode('utf-8')
        cr = csv.reader(decoded_content.splitlines(), delimiter=',')
        data = list(cr)
        df = pd.DataFrame(data[1:],columns=data[0])
        if len(data) < 10:
            raise IOError("Failed attempt")
        else:
            return df


# In[ ]:


# load the snp500 ticker data

df = pd.read_csv('data/Stock_indices/snp500_list.csv')
tickers = df.Symbol


# In[ ]:


directory = os.fsencode(local_path+'/cache/')

def aggregate(symbol):
    df = pd.read_pickle(local_path+'/cache/'+symbol+'_year1month2.pkl')
    for file in os.listdir(directory):
        filename = os.fsdecode(file)
        if filename.startswith(f'{symbol}_') and filename.endswith('.pkl'):
            df = pd.concat([df,pd.read_pickle(local_path+'/cache/'+filename)])
            #print(len(df),filename) 
            # uncomment this if you want some output just so that the code is running as expected
            os.remove(local_path+'/cache/'+filename)
            
        df.to_csv(local_path+'/cache/'+f'{symbol}.csv',index=False)
        
    return None  


# In[ ]:


for ticker in tickers[:1]:  #set the ticker range here
    for j in [1,2]:
        for string in [f'year{j}month{k}' for k in range(1,13)]:
            load_data(ticker,string)
            sleep(1)
            
    aggregate(ticker)

