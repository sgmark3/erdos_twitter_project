import streamlit as st
# import os
# import sys
# import inspect
# currentdir = os.path.dirname(os.path.abspath(inspect.getfile(inspect.currentframe())))
# parentdir = os.path.dirname(currentdir)
# sys.path.insert(0, parentdir) 
from Twitter_data_get import get_tweet_info as tweet
import pickle
from Twitter_Sentiment_Analysis.Text_to_Features_Script import get_text_analysis
import pandas as pd
import joblib
snp500_df = pd.read_csv("Raw_Data/Stock_indices/snp500_list.csv") 

def get_tweet_df(tweet_url):
    try:
        return tweet.get_info(tweet_url)    
    except:
        st.warning('Please check if tweet url is valid or try again!')
        st.session_state.text = ''
        #st.session_state.tweet_df = None
        tweet_url = None
        
def get_company_name(tweet_text):
    for i in range(len(snp500_df)):
        ticker = snp500_df['Symbol'].iloc[i]
        name = snp500_df['Security'].iloc[i].split(' ')[0]
        if '#'+ticker in str(tweet_text) or '$'+ticker in str(tweet_text) or name in str(tweet_text):
            print('found    ', name, ticker)
            return (ticker, name)
    return (0, 0)


def get_prediction(tweet_df, tweet_url):
    tweet_text = tweet_df['text'].iloc[0].split('\n')
    tweet_df = get_text_analysis(tweet_df)

    feature_columns = ['entities_cashtags', 'entities_hashtags', 'entities_urls',
                        'entities_mentions', 'public_metrics_followers_count', 'public_metrics_following_count',
                        'public_metrics_listed_count', 'public_metrics_tweet_count', 'Word_count_News_agencies',
                        'Word_count_Henry08_pos', 'Word_count_Henry08_neg',
                        'Word_count_LM11_pos', 'Word_count_LM11_neg',
                        'Word_count_Hagenau13_pos', 'Word_count_Hagenau13_neg',
                        'Tweet_Length_characters', 'Tweet_Length_words', 'Compound_vader',
                        'Positive_vader', 'Negative_vader', 'Neutral_vader']
    for col in tweet_df.columns:
        if col not in feature_columns:
            tweet_df=tweet_df.drop(col,axis=1)
    
    # get scaler used for modelling
    with open('web_app/rfc_scaler.pickle', 'rb') as f:
        scaler_ = pickle.load(f)
    tweet_df = pd.DataFrame(scaler_.transform(tweet_df), columns=tweet_df.columns)
    #st.text('Dataframe after scaling')
    #st.dataframe(tweet_df)
    st.markdown("###### Tweet text :")
    st.info("   \n  ".join(tweet_text))    
    
    # load saved model from pickle file, here its random
    model_ = joblib.load('web_app/randomforest_model.pickle')
    #print(tweet_df.info())

    x_new = tweet_df.iloc[0].values.reshape(1,-1)
    prediction= model_.predict( x_new )[0]
    print('Prediction = ', prediction)
    #prediction = 1
    
    popularity_precition = 'Popular'
    if prediction==0: popularity_precition = 'Not popular'
    # add model fitting and result here
    st.success('The tweet is predicted to be : ** {} ** '.format(popularity_precition))
    stock_movement = 'UP'
    if prediction:
        ticker, name = get_company_name(tweet_text)
        if ticker==0: 
            st.success('No stocks from SnP500 mentioned in tweet')
        else:            
            st.success('Expected stock price movement for {} ({}) : **{}**'.format(name, ticker, stock_movement))
        

    
def app():
    ## function gets tweet data and predictions
    st.title(' Tweet popularity ')
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
        print(" ******** using new values ************")
        tweet_df = get_tweet_df(tweet_url)
    else:
        print(" ******** using OLD values ************")
        tweet_df = st.session_state.tweet_df
    try:
        get_prediction(tweet_df, tweet_url)
        st.session_state.text = tweet_url
        st.session_state.tweet_df = tweet_df
    except:
        st.warning('Please check if tweet url is valid or try again!')
        st.session_state.text = None
        st.session_state.tweet_df = None
        tweet_url = None
        tweet_df = None
    #st.session_state.text = ''
    st.markdown('''
                # Details

            ** Strategies **  
            The setup uses Random Forest Classifier from Python's Scikit-Learn library to predict popularity of the given tweet using the tweet's features as input.
            
            ** Outcomes **  
            The model predict whether the given tweet is expected to be 'Popular' or 'Not popular'.

            ** Implementation **    
            [Github repository](https://github.com/msjithin/erdos_twitter_project)
            
            *** Disclaimer ** 
            This is part of a data scienc project and is not a recommendation for investing or trading.
            All investing and trading in the securities market involves risk. This is not a solicitation or recommendation 
            to buy or sell any stocks, options, or other financial instruments or investments.
                ''')
    
    
    