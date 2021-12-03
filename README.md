# Machine learning pipeline to extract a functional relationship between tweets and a stock's subsequent market reaction

[Web application link](https://share.streamlit.io/msjithin/erdos_twitter_project/main/web_app_main.py)

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

For the historic twitter data, we query the Twitter API for tweets from financially relevant Twitter accounts, such as Bloomberg, Yahoo Finance, The Economist, etc. from October 2019 to October 2021, and we filter the tweets for those that include either a company's full name, a hashtag of a company's stock ticker, or a cash tag of a company's stock ticker. The Twitter data was only pulled for those companies that are in the SP500 list, but our code could easily be generalized to include any or all companies that exist on any stock exchange.

We chose the above two-step filtering procedure (filtering via Twitter account and company mentions) due to the generally known, widespread presence of noise on Twitter. Surprisingly over the course of this project, we discovered that including simply the latter failed to sufficiently filter out noise, even when paired with additional filters such as the presence of financially relevant words. The result of our two-step filtering is that we recover Tweet data that is financially contextualized, and hence, we expect these tweets to serve as strong signals in predicting future market movement. Admittedly, this filtering procedure does forego other potentially strong signals such as a celebrity tweeting about a particular company or a given company tweeting about the release of a new project; the inclusion of such data is a potential direction for future work.

The raw Twitter data that we pull has the following attributes:

* The tweet text
* The mentions in a tweet
* The number of followers for the poster of the tweet
* The number of followings for the poster of the tweet
* The location of the the user
* The tweet's time stamp
* The tweet's hashtags and cashtags
* The URLs that appear in the tweet
* The number of likes, quotes, replies, and retweets of the tweet
* The tweet's listed count

In the data pre-processing section below, we detail which of these data attributes were kept and which were transformed or processed into a more useable way.

## Stock Dataset Description

For the historic stock data, we query the Alphavantage API for stock data pertaining to SP500 companies from March 2019 to March 2021. The time resolution of the stock prices is minute to minute. As twitter is a comparitively high frequency social media platform, we insisted on retaining minute to minute data, but unfortunately, this time resolution was only freely available over the aforementioned period. More extensive data for the purposes of backtesting can be obtained, albeit at substantial cost, via data repository sites such as [QuantQuote](https://quantquote.com/). We retain most of the standard asset data such as opening price, closing price, trading volume, 52 week high and lows.

# Data Pre-processing and Visualization

In order to make our data accessible via the machine learning algorithms of SKlearn, we first clean the data for anomalies and convert un-interpretable data into numerical values. That is, we convert the following Twitter data into simply a count of the number of each such occurence:

* URLs appearing in a tweet
* Hashtags appearing in a tweet
* Cashtags appearing in a tweet
* Other entities appearing in a tweet
* News agencies appearing in a tweet

For example, if there are two URLs that appear in a tweet, then we replace the column corresponding to the URLs with a count of two.

We are also concerned with the effects that a tweet's sentiment has on its popularity, we employ two metrics to determine tweet sentiment. The first is the use of the [Vader](https://github.com/cjhutto/vaderSentiment) natural language processing library. Vader has an advantage over other language processing libraries, because it is specifically designed to characterize the sentiment of social media data. That is, it incorporates slang terms, acronyms, and emojis- all of which are commonplace on social media. Secondly, we employ a word count of several word and bigram libraries that have appeared in the financial literature to characterize whether a tweet speaks positively or negatively about the underlying company or the companies' stock. The libraries that we use can be found at [(Henry, 2008)](https://journals.sagepub.com/doi/10.1177/0021943608319388), [(Loughran and Mcdonald, 2011)](https://onlinelibrary.wiley.com/doi/10.1111/j.1540-6261.2010.01625.x), and [(Hagenau, 2013)](https://www.researchgate.net/publication/254051649_Automated_News_Reading_Stock_Price_Prediction_Based_on_Financial_News_Using_Context-Specific_Features).

Finally, as the tweet prediction literature often explicitly employs time stamps, we  make three additional columns - morning, afternoon, and night that are derived from the the time stamp associated to when the tweet was made.

To gain a general sense for the relationships between each column of Twitter data, we have performed a preliminary, data visualization, which can be found in the
[Data_Visualization](https://github.com/msjithin/erdos_twitter_project/tree/main/Data_Visualization) directory of this Github repository.

# Machine Learning Piplines

In the below sub-sections, we detail the machine learning features and pipelines used in order to predict a tweet's popularity as well as the subsequent market movement. In each pipeline, we incorporate several models as well as several combinations of features in order to recover the best performing model.

## Prediction of Tweet Popularity

### Features

For the machine learning frameworks that we detail below, we use a variety of features from the pulled data, which are the following: the number of cashtags, the number of hashtags, the number of URLs, the number of mentions, the number of followers, the number of followings, the listed count, the number of tweets, the number of referenced news agencies, the positive and negative word and bigram counts associated with (Henry, 2008), (Loughran and Mcdonald, 2011), and (Hagenau, 2013), the number of characters in a tweet, the number of words in a tweet, the compound, positive, negative, and neutral Vader scores, and whether the tweet was made during the morning, evening or night.

Unfortunately, with a dataset of close to a million tweets and so many features, several of our machine learning implementations are prohibitively slow. Therefore, we use the [feature importance methods](https://scikit-learn.org/stable/auto_examples/ensemble/plot_forest_importances.html) of Sklearn to extract which features are most important and only use those features when computation time is a concern.

### Machine Learning Framework

In order to predict a tweet's popularity, we choose several, well established classifcation algorithms in the literature and compare their performance. In order to escape black-box hysteria and in the preservation of time, we limit ourselves to algorithms that we, the authors, have personally understood well. However, future work could certainly employ various other machine learning classification algorithms.

The classification frameworks that we adopt are the following:

* Logistic regression
* Random forests
* Decision trees paired with adaboost
* Light gradient boosting
* Naive Bayes

The classification problem is to predict when a particular feature will eclipse a certain threshold of likes. Throughout, this threshold is taken to be a hyperparameter, so that our code easily generalizes for any threshold of choice.

All of our machine learning code for prediction of tweet popularity can be found in the [ML_Model_Tweet_Prediction](https://github.com/msjithin/erdos_twitter_project/tree/main/ML_Model_Tweet_Prediction) directory of this Github repository.

## Prediction of Market Movement

### Features
Conditioning on the predictions of which tweets will become popular, we aggregate the tweet data with the stock data- pairing them temporally. The overall feature list then becomes all of the aforementioned tweet features as well as the following:
* Asset buy price
* Temporal distance between the buy price and the tweet's creation
* Temporal distance between the sell price and the tweet's creation

We compare our model's performance both with and without the above features for two reasons. The first is that the stock data is incomplete, and therefore, the temporal distances are somewhat randomly distributed amongst fixed time intervals. Secondly, due to this variation in the temporal distances, we want to ensure that there is no over-fitting within the model implementations. 

### Machine Learning Framework

In order to predict which tweets will lead to financial gains, we again choose several classification algorithms, which are the following:
* Naive Bayes
* Quadratic Disrciminat Analysis
* Random Forests

In future work, the author's would like to expand this list by looking to other classification techniques such as neural networks. In the above classification algorithms, our target is whether a return is positive or negative.  All of the relevant code can be found in the [ML_Model_Tweet_Prediction](https://github.com/msjithin/erdos_twitter_project/tree/main/ML_Model_Tweet_Prediction) directory of this Github repository. 
