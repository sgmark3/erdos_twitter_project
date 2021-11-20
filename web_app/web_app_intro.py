import numpy as np
import matplotlib.pyplot as plt
from matplotlib.patches import Rectangle
from scipy.stats import norm
import streamlit as st
import Twitter_data_get.get_tweet_info as tweet


def app():

    st.markdown('''
    Enter tweet url 
    ''')
    st.title('** title **')
    default_tweet = 'https://twitter.com/markets/status/1458402478123327497'
    tweet_url = str(st.text_input("Current Price", default_tweet))
    tweet_df = tweet.get_info(tweet_url)    
    st.dataframe(tweet_df)

