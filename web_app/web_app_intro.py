import numpy as np
import matplotlib.pyplot as plt
from matplotlib.patches import Rectangle
from scipy.stats import norm
import streamlit as st
import Twitter_data_get.get_tweet_info as tweet


def app():


    st.title('** Tweet analysis **')
    st.markdown('''
    
    ''')
    default_tweet = 'https://twitter.com/markets/status/1458402478123327497'
    tweet_url = str(st.text_input("Enter tweet url ", default_tweet))
    tweet_df = tweet.get_info(tweet_url)    
    tweet_text = tweet_df['text'].iloc[0]

    st.dataframe(tweet_df)
    st.markdown("###### Tweet text :")
    st.text(tweet_text)

    