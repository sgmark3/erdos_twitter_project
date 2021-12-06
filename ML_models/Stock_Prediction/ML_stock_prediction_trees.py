from sklearn.linear_model import LogisticRegression
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler
from sklearn.model_selection import StratifiedKFold
from sklearn.naive_bayes import GaussianNB, BernoulliNB

from sklearn.tree import DecisionTreeClassifier as dfc
from sklearn.ensemble import RandomForestClassifier as rfc
from sklearn.ensemble import AdaBoostClassifier, GradientBoostingClassifier
from sklearn.metrics import classification_report, confusion_matrix, accuracy_score, roc_auc_score

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

# Load the parquet data of tweets
local_path = '/Users/Andrew/Desktop/median_tweet_stock.parquet'
tweetframe = pd.read_parquet(local_path)
#tweetframe = tweetframe[tweetframe['delta_buy']<5000]
# Random Forest Classifier for predicting which tweets become popular


def multiple_time_frames(tweetframe, threshold):

    l = len(tweetframe)
    tweetframe_copy = tweetframe.copy()
    tweetframe1 = tweetframe_copy.iloc[:l//3,:]
    tweetframe2 = tweetframe_copy.iloc[l//3:2*l//3,:]
    tweetframe3 = tweetframe_copy.iloc[2*l//3:,:]

    pred1 = random_forest(tweetframe1, threshold)
    pred2 = random_forest(tweetframe2, threshold)
    pred3 = random_forest(tweetframe3, threshold)

    tweetframe_pred_1 = pred1[pred1['prediction']==1]
    tweetframe_pred_2 = pred2[pred2['prediction']==1]
    tweetframe_pred_3 = pred3[pred3['prediction']==1]

    return tweetframe_pred_1, tweetframe_pred_2, tweetframe_pred_3

    # Random Forest Classifier for predicting which tweets become popular
def random_forest_returns(tweetframe, threshold):
    # Step 1: Get Features
    tweetframe['good_return'] = tweetframe['return'].apply(lambda x: 1 if x >= threshold else 0)
    feature_columns = ['entities_cashtags', 'entities_hashtags', 'entities_urls',
                       'entities_mentions', 'followers_count', 'following_count',
                       'listed_count', 'tweet_count', 'Word_count_News_agencies',
                       'Word_count_Henry08_pos', 'Word_count_Henry08_neg',
                       'Word_count_LM11_pos', 'Word_count_LM11_neg',
                       'Word_count_Hagenau13_pos', 'Word_count_Hagenau13_neg',
                       'Tweet_Length_characters', 'Tweet_Length_words', 'Compound_vader',
                       'Positive_vader', 'Negative_vader', 'Neutral_vader', 'morning',
                       'evening', 'night', 'delta_buy', 'buy_price']

    # Step 2: Establish train, test split
    X_train, X_test, Y_train, Y_test = train_test_split(tweetframe[feature_columns].copy(),
                                                        tweetframe['good_return'].copy(),
                                                        test_size=.2,
                                                        random_state=407,
                                                        shuffle=True, stratify =tweetframe['good_return'])
    # Step 3: Scale the data
    sc = StandardScaler()
    X_train = sc.fit_transform(X_train)
    X_test = sc.fit_transform(X_test)

    # Step 3: Establish model
    classifier = rfc(max_depth=50)
    classifier.fit(X_train, Y_train)
    y_pred = classifier.predict(X_test)
    y_pred1 = classifier.predict(tweetframe[feature_columns])
    prob = classifier.predict_proba(tweetframe[feature_columns])

    # Step 4: Check model validity
    conf_matrix = confusion_matrix(Y_test, y_pred)
    class_report = classification_report(Y_test, y_pred)
    accuracy = accuracy_score(Y_test, y_pred)
    roc_auc = roc_auc_score(Y_test, y_pred)

    return y_pred1,prob, roc_auc, class_report, accuracy, [feature_columns, classifier.feature_importances_]

def adaboost_decision_tree_returns(tweetframe, threshold):
    # Step 1: Get Features
    tweetframe['good_return'] = tweetframe['return'].apply(lambda x: 1 if x > threshold else 0)
    feature_columns = ['Word_count_Henry08_pos', 'Word_count_Henry08_neg',
                       'Word_count_LM11_pos', 'Word_count_LM11_neg',
                       'Word_count_Hagenau13_pos', 'Word_count_Hagenau13_neg',
                        'Compound_vader',]
    # Step 2: Establish train, test split
    X_train, X_test, Y_train, Y_test = train_test_split(tweetframe[feature_columns].copy(),
                                                        tweetframe['good_return'].copy(),
                                                        test_size=.2,
                                                        random_state=407,
                                                        shuffle=True, stratify =tweetframe['good_return'])
    # Step 3: Scale the data
    sc = StandardScaler()
    X_train = sc.fit_transform(X_train)
    X_test = sc.fit_transform(X_test)

    # Step 3: Establish model
    ada = AdaBoostClassifier(dfc(max_depth=100, max_leaf_nodes =20))
    ada.fit(X_train, Y_train)
    Y_pred = ada.predict(X_test)

    # Step 4: Check model validity
    conf_matrix = confusion_matrix(Y_test, Y_pred)
    class_report = classification_report(Y_test, Y_pred)
    accuracy = accuracy_score(Y_test, Y_pred)

    return class_report, accuracy

tweetframe_pop = tweetframe[tweetframe['like_count']>=20].copy()

y_pred, prob, roc_auc, class_report, accuracy, vec_random = random_forest_returns(tweetframe_pop, 0)


print('The Random Forest class report is: \n', class_report)
print('The Random Forest accuracy score is: ', accuracy)
print('The Random Forest roc auc score is: ', roc_auc)
tweetframe_pop['predicted_returns'] = y_pred
print(tweetframe.shape)
my_list = []
for i in range(len(tweetframe_pop)):
    if tweetframe_pop['predicted_returns'].iloc[i]==1:
        my_list.append(tweetframe_pop['return'].iloc[i]/100)
my_series = pd.Series(my_list)
print(my_series)
print(max(my_series), my_series.mean(), my_series.sum())
my_returns = ((1+my_series).cumprod()-1)
print(my_returns)
#plt.hist(prob)
plt.show()
plt.plot(my_returns)
plt.show()
