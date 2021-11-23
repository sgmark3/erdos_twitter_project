import streamlit as st
import Twitter_data_get.get_tweet_info as tweet
import pickle
from Twitter_Sentiment_Analysis.Text_to_Features_Script import get_text_analysis
import pandas as pd


def get_tweet_df(tweet_url):
    try:
        return tweet.get_info(tweet_url)    
    except:
        st.warning('Please check if tweet url is valid or try again!')
        st.session_state.text = ''
        #st.session_state.tweet_df = None
        tweet_url = None
        
        
def get_prediction(tweet_df, tweet_url):
    tweet_text = tweet_df['text'].iloc[0].split('\n')
    tweet_df = get_text_analysis(tweet_df)
    parameters_to_keep = ['entities_hashtags', 'entities_cashtags','entities_urls','public_metrics_followers_count',
                'public_metrics_following_count', 'public_metrics_listed_count','public_metrics_tweet_count','media_type','entities_mentions',
                'Word_count_Henry08_pos', 'Word_count_Henry08_neg',
                'Word_count_LM11_pos', 'Word_count_LM11_neg',
                'Word_count_Hagenau13_pos', 'Word_count_Hagenau13_neg',
                'Tweet_Length_characters', 'Compound_vader','Positive_vader', 'Negative_vader', 'Neutral_vader']

    for col in tweet_df.columns:
        if col not in parameters_to_keep:
            tweet_df=tweet_df.drop(col,axis=1)
    st.text('Dataframe before scaling')
    st.dataframe(tweet_df)
    with open('web_app/lgbm_scaler.pickle', 'rb') as f:
        scaler_ = pickle.load(f)
    tweet_df = pd.DataFrame(scaler_.transform(tweet_df), columns=tweet_df.columns)
    st.text('Dataframe after scaling')
    st.dataframe(tweet_df)
    st.markdown("###### Tweet text :")
    st.info("   \n  ".join(tweet_text))    
    #st.text_area(label="Tweet text ", value="   \n  ".join(tweet_text), height=20 )

    # ## setting session states
    # st.session_state.text = tweet_url
    # st.session_state.tweet_df = tweet_df
    
    # if sesion state tweet_df is None or unchanged, get model and get fit again
    # else prediction = st.session_state.prediction
    with open('web_app/lgbm_model.pickle', 'rb') as f:
        model_ = pickle.load(f)

    #print(tweet_df.info())

    x_new = tweet_df.iloc[0].values.reshape(1,-1)
    prediction= model_.predict( x_new )[0]
    print('Prediction = ', prediction)
    #prediction = 1
    
    popularity_precition = 'Popular'
    if prediction==0: popularity_precition = 'Not popular'
    # add model fitting and result here
    st.success('The tweet is predicted to be : ** {} ** '.format(popularity_precition))
    ticker_name = 'TSLA'
    stock_movement = 'UP'
    st.success('Expected stock price movement for ticker **{}** is : **{}**'.format(ticker_name, stock_movement))

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
        #print(" ******** using new values ************")
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
        st.session_state.text = ''
        #st.session_state.tweet_df = None
        tweet_url = None
        tweet_df = None
    st.session_state.text = ''
    st.markdown('''
                # Details

            ** Strategies **  

            ** Outcomes **  
            The model predict whether the given tweet is expected to be 'Popular' or 'Not popular'.

            ** Implementation **    
            [Github repository](https://github.com/msjithin/erdos_twitter_project)
                ''')
    
    
    