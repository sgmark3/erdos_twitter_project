import streamlit as st
import streamlit.components.v1 as components
from PIL import Image
image_feature_imp = Image.open('web_app/images/feature_importance_RFC.png')
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
''')

    components.html('''
    <!DOCTYPE html>
    <html>
    <head>
    <style>
    #h2 {
    font-family: Arial, Helvetica, sans-serif;
    border-collapse: collapse;
    width: 100%;
    }
    #models {
    font-family: Arial, Helvetica, sans-serif;
    border-collapse: collapse;
    width: 100%;
    }

    #models td, #models th {
    border: 1px solid #ddd;
    padding: 8px;
    }

    #models tr:nth-child(even){background-color: #f2f2f2;}

    #models tr:hover {background-color: #ddd;}

    #models th {
    padding-top: 12px;
    padding-bottom: 12px;
    text-align: left;
    background-color: #04AA6D;
    color: white;
    }
    </style>
    </head>
    <body>

    <h2 id="h2">Models</h2>

    <table id="models">
    <tr>
        <th>Model</th>
        <th>Accurary</th>
        <th>Precision</th>
        <th>Recall</th>
        <th>F1 score</th>
        <th>ROC AUC</th>
    </tr>
    
        <tr>
        <td>Random Forests</td><td>0.8871</td><td>0.8869</td><td>0.8871</td><td>0.8869</td><td>0.8827</td>
        </tr>
        <tr>
        <td>Adaboost</td><td>0.8673</td><td>0.8680</td><td>0.8672</td><td>0.8675</td><td>0.8654</td>
        </tr>   
        <tr>
        <td>Light Gradient boosting</td><td>0.8633</td><td>0.8710</td><td>0.8124</td><td>0.8627</td><td> 0.8581  </td>
        </tr>
        <tr>
        <td>Logistic Regression</td><td>0.7397</td><td> 0.75 </td><td> 0.74 </td><td>0.7405</td><td> 0.7429 </td>
        </tr>
        <tr>
        <td>Naive Bayes</td><td>0.6947</td><td> 0.73 </td><td> 0.69 </td><td>0.6910</td><td> 0.7111  </td>
        </tr>
    </table>

    </body>
    </html
    ''', height=350)
    st.image(image_feature_imp, caption='Feature importance for Random Forest model')
    st.markdown('''
    All of our machine learning code for prediction of tweet popularity can be found in the [ML_Model_Tweet_Prediction](https://github.com/msjithin/erdos_twitter_project/tree/main/ML_Model_Tweet_Prediction) directory of this Github repository.

    ## Prediction of Market Movement

    ### Features

    ### Machine Learning Framework  
        ''')
