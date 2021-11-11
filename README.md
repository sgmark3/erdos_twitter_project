# Machine learning pipeline to extract a functional relationship between tweets and a stock's subsequent market reaction

# Team Members:
- [Jose A. Fortou](https://www.linkedin.com/in/jose-a-fortou-01957b214/)
- [Jithin Madhusudanan Sreekala](https://www.linkedin.com/in/jithinms)
- [Shashank Markande](https://www.linkedin.com/in/smarkande)
- [Andrew McMillan](https://www.linkedin.com/in/andrew-mcmillan-68983b96)
- [Yossathorn (Josh) Tawabutr](https://www.linkedin.com/in/yossathorn-tawabutr)

# Introduction and Motivation
This Github repository is devoted to completing the [Erdos Institute](https://www.erdosinstitute.org/), data science bootcamp project to obtain a certificate of competence and excellence in the techniques of data science and more specifically machine learning. We would first like to graciously thank the constituents of the Erdos institute for their incredibale guidance, encouragement, and resources while this project was undertaken. 

Our project stems from the corporate sponsored [Susquehanna](https://sig.com/) project which challenges participants to develop a machine learning framework to predict tweet popularity. Many such projects and solution attempts have appeared both in the academic literature as well as in other public sources, such as Github and various data science discussion forums. Therefore, we have chosen to build on the prompt by extending our project into a novel, financial context. 

The first direction is to do just as the prompt suggests, so we collect Twitter data from various sources and attempt to predict the popularity of tweets based on various features that are exclusive to twitter, such as a user's number of followers, number of historic tweets, length of the tweet, etc., and we pair these features with those generated via [natural language processing](https://en.wikipedia.org/wiki/Natural_language_processing) and libraries of historically positive and negative words in order to establish the [sentiment](https://en.wikipedia.org/wiki/Sentiment_analysis) of a tweet. 

The second direction is to then predict the movement of asset prices while conditioning on the results of the predicted tweet popularity. That is, we hypothesize that market movements will generally be affected by tweets that receive widespread attention, and by using the predicted tweets as initial data, we can potentially gain a first mover advantage in the market. To the author's knowledge, this is the first such a coupling of the first and second direction has appeared publicly. 
# Data Gathering
We gather historic data from both Twitter and the stock market using the [Twitter API](https://developer.twitter.com/en/docs) and the [AlphaVantage API](https://www.alphavantage.co/), respectively. The descriptions of both data sets can be found below.  
### Dataset Description
For the historic twitter data, we query the Twitter API for tweets from financially relevant Twitter accounts, such as Bloomberg, Yahoo Finance, The Economist, etc., and we filter the tweets for those that include either a company's full name, a hashtag of a company's stock ticker, or a cash tag of a company's stock ticker. The Twitter data was only pulled for those companies that comprise the SP500, but our code could easily be generalized to include any or all companies that exist on any stock exchange.  
### Data Pre-processing


# Machine Learning Piplines
## Prediction of Tweet Popularity
### Features
### Machine Learning Framework
## Prediction of Market Movement
### Features
### Machine Learning Framework
