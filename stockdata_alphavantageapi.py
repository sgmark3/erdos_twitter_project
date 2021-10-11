#!/usr/bin/env python
# coding: utf-8

# In[1]:


import numpy as np
import os
import requests
from bs4 import BeautifulSoup
import pandas as pd
import re
from datetime import datetime


# ### The stock price data from Alphavantage python API

# In[2]:


def load_data(t):
    url = 'https://www.alphavantage.co/query?function=TIME_SERIES_INTRADAY&symbol=' + t + '&interval=1min&apikey=' + api_key
    r = requests.get(url)
    data = r.json()
    df = pd.DataFrame(data['Time Series (1min)']).transpose()
    df['date_time'] = [datetime.strptime(entry,"%Y-%m-%d %H:%M:%S") for entry in df.index]
    return df


# In[4]:


load_data('MSFT').head(5)


# ### S&P 500 companies tickers (only up to top 500 companies)

# In[5]:


response = requests.get('https://en.wikipedia.org/wiki/List_of_S%26P_500_companies')
response.status_code
soup =  BeautifulSoup(response.text, "lxml")
trs = soup.findAll('tr')
headings = []
for entry in trs[0].findAll('th'):
    headings.append(entry.text.strip())

tickers = {}
for item in trs[1:501]:
    i = 0
    values = []
    for entry in item.findAll('td'):
        if i == 0:
            key = entry.text.strip()
        else:
            values.append(entry.text.strip())
        i = i + 1
    tickers[key] = values
    
df = pd.DataFrame(tickers.values(),columns = headings[1:])
df['TICKER'] = tickers.keys()
df = df.set_index('TICKER')


# In[6]:


df.head(5)


# In[8]:


#tickers      #dictionary with firm name and other information as shown in the dataframe above, uncomment to check




