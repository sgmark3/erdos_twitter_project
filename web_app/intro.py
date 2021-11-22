
import streamlit as st

def app():
    st.title(' Tweet popularity ')

    st.markdown('''
    # Introduction and Motivation 

    This Github repository is devoted to completing the [Erdos Institute](https://www.erdosinstitute.org/), data science bootcamp project to obtain a certificate of competence and excellence in the techniques of data science and more specifically machine learning. We would first like to graciously thank the constituents of the Erdos institute for their incredible guidance, encouragement, and resources while this project was undertaken.

    Our project stems from the corporate sponsored [Susquehanna](https://sig.com/) project which challenges participants to develop a machine learning framework to predict tweet popularity. Many such projects and solution attempts have appeared both in the academic literature as well as in other public sources, such as Github and various data science discussion forums. Therefore, we have chosen to build on the prompt by extending our project into a novel, financial context.

    The first direction is to do just as the prompt suggests, so we collect Twitter data from various sources and attempt to predict the popularity of tweets based on various features that are exclusive to twitter, such as a user's number of followers, number of historic tweets, length of the tweet, etc., and we pair these features with those generated via [natural language processing](https://en.wikipedia.org/wiki/Natural_language_processing) and libraries of historically positive and negative words in order to establish the [sentiment](https://en.wikipedia.org/wiki/Sentiment_analysis) of a tweet.

    The second direction is to then predict the movement of asset prices while conditioning on the results of the predicted tweet popularity. That is, we hypothesize that market movements will generally be affected by tweets that receive widespread attention, and by using the predicted tweets as initial data, we can potentially gain a first mover advantage in the market. To the author's knowledge, this is the first time such a coupling of the first and second direction has appeared publicly.    
        
    ''')
    


