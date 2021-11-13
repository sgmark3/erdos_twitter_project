import pandas as pd
import pandas_datareader.data as web
import numpy as np
import requests, time, re, pickle
from config import *
import json

"""
Api details 
https://developer.tdameritrade.com/apis
"""
base_url = "https://api.tdameritrade.com"
instrument_url = 'https://api.tdameritrade.com/v1/instruments'
option_url = 'https://api.tdameritrade.com/v1/marketdata/chains'

symbols = ['AAPL', 'FB']

def get_fundamentals(ticker=""):
    start, end = 0, 500
    
    payload = {'apikey': ameritrade_key ,
            'symbol':ticker,
            'projection':'fundamental'
            }
    results = requests.get(instrument_url, params=payload)
    data = results.json()
    return data
       
def get_historical(ticker="", period_type="day", period=2, frequency=1, frequency_type="min" ):
    """
    reference:
    https://developer.tdameritrade.com/price-history/apis/get/marketdata/%7Bsymbol%7D/pricehistory
    """
    # watch out for period_type - frequency_type relations , not all combinations worked.
    start, end = 0, 500
    payload = {'apikey': ameritrade_key,
        'periodType' : period_type,
        'period' : period
            }
    #url_to_use = base_url+"/v1/marketdata/AAPL/pricehistory?apikey=JYMFWADLTIEXG6NASXYVSZ0FQLVRKUX8&periodType=year&period=2&frequencyType=daily&frequency=1"
    url_to_use = base_url + "/v1/marketdata/AAPL/pricehistory"
    results = requests.get(url_to_use, params=payload)
    data = results.json()
    return data

def get_option_data(ticker=""):
    start, end = 0, 500
    
    payload = {'apikey':  ameritrade_key ,
            'symbol':ticker,
            'contractType' : 'CALL',
            'strikeCount' : 2,
            'includeQuotes' : True,
            'strategy' :'ANALYTICAL'
            }
    results = requests.get(option_url, params=payload)
    data = results.json()
    return data

def check_nested_dict(d):
    return any(isinstance(i,dict) for i in d.values())

def write_on_page():
    pass
def fundamental(stock_name=""):
    if stock_name is None:
        return
    return get_fundamentals(stock_name)
    


def option_data(stock_name=""):
    if stock_name is None:
        return
    return get_option_data(stock_name)
    
     
if __name__ == "__main__":
    ticker_name = 'AAPL'
    # print(option_data(ticker_name))
    # print(fundamental(ticker_name))
    #print(get_historical(ticker_name))
    with open(ticker_name+'.json', 'w') as outfile:
        json.dump(get_historical(ticker_name), outfile, indent=4, sort_keys=True)
