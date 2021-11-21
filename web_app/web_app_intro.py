import numpy as np
import matplotlib.pyplot as plt
from matplotlib.patches import Rectangle
from scipy.stats import norm
import streamlit as st
import Twitter_data_get.get_tweet_info as tweet

def get_tweet_df(tweet_url):
    return tweet.get_info(tweet_url)    


def app():
    ## function gets tweet data and predictions
    st.title('** Tweet analysis **')
    st.markdown('''
    
    ''')
    default_tweet = 'https://twitter.com/markets/status/1458402478123327497' # setting default tweet url
    # check if state of page is same as before
    # this keeps text input unchanged when navigating tabs
    if st.session_state.text is None:              # check if state of page is same as before
        st.session_state.text = default_tweet
    tweet_url = str(st.text_input("Enter tweet url ", st.session_state.text))
    
    # check if state of page is same as before
    # this keeps dataframe unchanged when navigating tabs
    if (st.session_state.tweet_df is None) or (st.session_state.text != tweet_url ):
        #print(" ******** using new values ************")
        tweet_df = get_tweet_df(tweet_url)
    else:
        #print(" ******** using OLD values ************")
        tweet_df = st.session_state.tweet_df

    tweet_text = tweet_df['text'].iloc[0].split('\n')

    st.dataframe(tweet_df)
    st.markdown("###### Tweet text :")
    st.info("   \n  ".join(tweet_text))    
    #st.text_area(label="Tweet text ", value="   \n  ".join(tweet_text), height=20 )

    ## setting session states
    st.session_state.text = tweet_url
    st.session_state.tweet_df = tweet_df
    
