
import streamlit as st

def app():
    st.title(' Tweet popularity ')

    st.markdown('''
# Prediction of Tweet Popularity

### Features

For the machine learning frameworks that we detail below, we use a variety of features from the pulled data, which are the following: the number of cashtags, the number of hashtags, the number of URLs, the number of mentions, the number of followers, the number of followings, the listed count, the number of tweets, the number of referenced news agencies, the positive and negative word and bigram counts associated with (Henry, 2008), (Loughran and Mcdonald, 2011), and (Hagenau, 2013), the number of characters in a tweet, the number of words in a tweet, the compound, positive, negative, and neutral Vader scores, and whether the tweet was made during the morning, evening or night.

Unfortunately, with a dataset of close to a million tweets and so many features, several of our machine learning implementations are prohibitively slow. Therefore, we use the [feature importance methods](https://scikit-learn.org/stable/auto_examples/ensemble/plot_forest_importances.html) of Sklearn to extract which features are most important and only use those features when computation time is a concern.

### Machine Learning Framework

In order to predict a tweet's popularity, we choose several, well established classifcation algorithms in the literature and compare their performance. In order to escape black-box hysteria and in the preservation of time, we limit ourselves to algorithms that we, the authors, have personally understood well. However, future work could certainly employ various other machine learning classification algorithms.

The classification frameworks that we adopt are the following:

* Logistic regression
* K nearest neighbors
* Random forests
* Decision trees paired with adaboost
* Light gradient boosting
* Naive Bayes

The classification problem is to predict when a particular feature will eclipse a certain threshold of likes. Throughout, this threshold is taken to be a hyperparameter, so that our code easily generalizes for any threshold of choice.

All of our machine learning code for prediction of tweet popularity can be found in the [ML_Model_Tweet_Prediction](https://github.com/msjithin/erdos_twitter_project/tree/main/ML_Model_Tweet_Prediction) directory of this Github repository.

## Prediction of Market Movement

### Features

### Machine Learning Framework  
    ''')