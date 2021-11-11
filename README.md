# Machine learning pipeline to extract a functional relationship between tweets and a stock's subsequent market reaction

# Team Members:
- [Jithin Madhusudanan Sreekala](https://www.linkedin.com/in/jithinms)
- [Shashank Markande](https://www.linkedin.com/in/smarkande)
- [Andrew McMillan](https://www.linkedin.com/in/andrew-mcmillan-68983b96)
- [Yossathorn (Josh) Tawabutr](https://www.linkedin.com/in/yossathorn-tawabutr)

# Introduction and Motivation
This Github repository is devoted to completing the [Erdos Institute](https://www.erdosinstitute.org/), data science bootcamp project to obtain a certificate of competence and excellence in the techniques of data science and more specifically machine learning. We would first like to graciously thank the constituents of the Erdos institute for their incredible guidance, encouragement, and resources while this project was undertaken. 

Our project stems from the corporate sponsored [Susquehanna](https://sig.com/) project which challenges participants to develop a machine learning framework to predict tweet popularity. Many such projects and solution attempts have appeared both in the academic literature as well as in other public sources, such as Github and various data science discussion forums. Therefore, we have chosen to build on the prompt by extending our project into a novel, financial context. 

The first direction is to do just as the prompt suggests, so we collect Twitter data from various sources and attempt to predict the popularity of tweets based on various features that are exclusive to twitter, such as a user's number of followers, number of historic tweets, length of the tweet, etc., and we pair these features with those generated via [natural language processing](https://en.wikipedia.org/wiki/Natural_language_processing) and libraries of historically positive and negative words in order to establish the [sentiment](https://en.wikipedia.org/wiki/Sentiment_analysis) of a tweet. 

The second direction is to then predict the movement of asset prices while conditioning on the results of the predicted tweet popularity. That is, we hypothesize that market movements will generally be affected by tweets that receive widespread attention, and by using the predicted tweets as initial data, we can potentially gain a first mover advantage in the market. To the author's knowledge, this is the first time such a coupling of the first and second direction has appeared publicly. 
# Data Gathering
We gather historic data from both Twitter and the stock market using the [Twitter API](https://developer.twitter.com/en/docs) and the [AlphaVantage API](https://www.alphavantage.co/), respectively. The descriptions of both data sets can be found below.  

## Twitter Dataset Description
For the historic twitter data, we query the Twitter API for tweets from financially relevant Twitter accounts, such as Bloomberg, Yahoo Finance, The Economist, etc. from March 2019 to March 2021, and we filter the tweets for those that include either a company's full name, a hashtag of a company's stock ticker, or a cash tag of a company's stock ticker. The Twitter data was only pulled for those companies that comprise the SP500, but our code could easily be generalized to include any or all companies that exist on any stock exchange. 

We chose the above two-step filtering procedure (filtering via Twitter account and company mentions) due to the generally known, widespread presence of noise on Twitter. Surprisingly over the course of this project, we discovered that including simply the latter failed to sufficiently filter out noise, even when paired with additional filters such as the presence of financially relevant words. The result of our two-step filtering is that we recover Tweet data that is financially contextualized, and hence, we expect these tweets to serve as strong signals in predicting future market movement. Admittedly, this filtering procedure does forego other potentially strong signals such as a celebrity tweeting about a particular company or a given company tweeting about the release of a new project; the inclusion of such data is a potential direction for future work. 


The resulting, aggregated dataset comprises of 914,000 tweets from March 2019 to March 2021 and can be found in the [Data_Preprocessed](https://github.com/msjithin/erdos_twitter_project/tree/main/Data/Data_Preprocessed) directory of this Github repository.  

## Stock Dataset Description
For the historic stock data, we query the Alphavantage API for stock data pertaining to SP500 companies from March 2019 to March 2021. The time resolution of the stock prices is minute to minute. As twitter is a comparitively high frequency social media platform, we insisted on retaining minute to minute data, but unfortunately, this time resolution was only freely available over the aforementioned period. More extensive data for the purpose of backtesting can be obtained, albeit at substantial cost, via data repository sites such as [QuantQuote](https://quantquote.com/).

We retain most of the standard asset data such as opening price, closing price, trading volume, 52 week high and lows, but as our primary task is the effect of popular tweets on asset movements, we only incorporate opening and closing prices in our resulting machine learning framework.
# Data Pre-processing and Visualization
In order to make our data accessible via the machine learning algorithms of SKlearn, we first clean the data for anomalies and convert un-interpretable data into numerical values. That is, we convert the following Twitter data into simply a count of the number of each such occurence:
* URLs appearing in a tweet
* Hashtags appearing in a tweet
* Cashtags appearing in a tweet
* Other entities appearing in a tweet

For example, if there are two URLs that appear in a tweet, then we replace the column corresponding to the URLs with a count of two.

# Machine Learning Piplines
In the below sub-sections, we detail the machine learning features and pipelines used in order to predict a tweet's popularity as well as the subsequent market movement. In each pipeline, we incorporate several models as well as several pairings of features in order to recover the best performing model.
## Prediction of Tweet Popularity
### Features
### Machine Learning Framework
In order to predict a tweet's popularity, we choose several, well established classifcation algorithms in the literature and compare their performance. In order to escape black-box hysteria and in the preservation of time, we limit ourselves to algorithms that we, the authors, have personally understood well. However, future work could certainly employ various other machine learning classification algorithms. 

The classification frameworks that we adopt are the following: logistic regression, k nearest neighbors, random forests, decision trees paired with adaboost, light gradient boosting, and xgboost. All of our code can be found in the [ML_Model_Tweet_Prediction](https://github.com/msjithin/erdos_twitter_project/tree/main/ML_Model_Tweet_Prediction) directory of this Github repository. 
## Prediction of Market Movement
### Features
### Machine Learning Framework
