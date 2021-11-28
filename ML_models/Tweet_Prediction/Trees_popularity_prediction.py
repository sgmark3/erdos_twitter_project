from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler
from sklearn.model_selection import StratifiedKFold

from sklearn.tree import DecisionTreeClassifier as dfc
from sklearn.ensemble import RandomForestClassifier as rfc
from sklearn.ensemble import AdaBoostClassifier
from sklearn.metrics import classification_report, confusion_matrix, accuracy_score

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

# Load the parquet data of tweets
local_path = '/Users/Andrew/Desktop/shashank_tweet_temporal.parquet'
tweetframe = pd.read_parquet(local_path)


# Random Forest Classifier for predicting which tweets become popular
def random_forest(tweetframe, threshold):
    # Step 1: Get Features
    tweetframe['popularity'] = tweetframe['like_count'].apply(lambda x: 1 if x >= threshold else 0)
    feature_columns = ['entities_cashtags', 'entities_hashtags', 'entities_urls',
                       'entities_mentions', 'followers_count', 'following_count',
                       'listed_count', 'tweet_count', 'Word_count_News_agencies',
                       'Word_count_Henry08_pos', 'Word_count_Henry08_neg',
                       'Word_count_LM11_pos', 'Word_count_LM11_neg',
                       'Word_count_Hagenau13_pos', 'Word_count_Hagenau13_neg',
                       'Tweet_Length_characters', 'Tweet_Length_words', 'Compound_vader',
                       'Positive_vader', 'Negative_vader', 'Neutral_vader', 'morning', 'evening', 'night']

    # Step 2: Establish train, test split
    X_train, X_test, Y_train, Y_test = train_test_split(tweetframe[feature_columns].copy(),
                                                        tweetframe['popularity'].copy(),
                                                        stratify = tweetframe['popularity'].copy(),
                                                        test_size=.2,
                                                        random_state=407,
                                                        shuffle=True)
    # Step 3: Scale the data
    sc = StandardScaler()
    X_train = sc.fit_transform(X_train)
    X_test = sc.fit_transform(X_test)

    # Step 3: Establish model
    classifier = rfc(max_depth=30)
    classifier.fit(X_train, Y_train)
    Y_pred = classifier.predict(X_test)

    # Step 4: Check model validity
    conf_matrix = confusion_matrix(Y_test, Y_pred)
    class_report = classification_report(Y_test, Y_pred)
    accuracy = accuracy_score(Y_test, Y_pred)

    return class_report, accuracy, [feature_columns, classifier.feature_importances_]

# Use Kfold cross validation and random forests to back out which tree depth is optimal
def random_forest_cross_valid(tweetframe, threshold):
    # Step 1: Get Features
    tweetframe['popularity'] = tweetframe['public_metrics_like_count'].apply(lambda x: 1 if x >= threshold else 0)
    feature_columns = ['entities_cashtags', 'entities_hashtags', 'entities_urls', 'entities_mentions',
                       'public_metrics_followers_count', 'public_metrics_following_count',
                       'public_metrics_tweet_count', 'Tweet_Length_characters', 'Tweet_Length_words',
                       'Word_count_News_agencies', 'Compound_vader', 'Neutral_vader', 'Positive_vader',
                       'Negative_vader']

    # Step 2: Establish train, test split
    max_depth = 30
    X = tweetframe[feature_columns].copy()
    y = tweetframe['popularity'].copy()
    forest_cv_accs = np.zeros((5, max_depth))
    max_depths = range(10, max_depth + 1)

    kfold = StratifiedKFold(5, shuffle=True, random_state=194)
    sc = StandardScaler()
    # X = sc.fit_transform(X)

    i = 0
    for train_index, test_index in kfold.split(X, y):
        X_train = X.loc[train_index]
        X_holdout = X.loc[test_index]

        y_train = y.loc[train_index]
        y_holdout = y.loc[test_index]
        j = 0
        for depth in max_depths:
            forest = rfc(n_estimators=100, random_state=512, max_depth=depth)

            forest.fit(X_train, y_train)
            forest_cv_accs[i, j] = accuracy_score(y_holdout, forest.predict(X_holdout))
            print(i, j)
            j = j + 1
        i = i + 1
    return forest_cv_accs, max_depths

# Use adaboost paired with decision trees to classify which tweets will become popular
def adaboost_decision_tree(tweetframe, threshold):
    # Step 1: Get Features
    tweetframe['popularity'] = tweetframe['like_count'].apply(lambda x: 1 if x >= threshold else 0)
    feature_columns = ['entities_cashtags', 'entities_hashtags', 'entities_urls',
                       'entities_mentions', 'followers_count', 'following_count',
                       'listed_count', 'tweet_count', 'Word_count_News_agencies',
                       'Word_count_Henry08_pos', 'Word_count_Henry08_neg',
                       'Word_count_LM11_pos', 'Word_count_LM11_neg',
                       'Word_count_Hagenau13_pos', 'Word_count_Hagenau13_neg',
                       'Tweet_Length_characters', 'Tweet_Length_words', 'Compound_vader',
                       'Positive_vader', 'Negative_vader', 'Neutral_vader', 'morning', 'evening', 'night']

    # Step 2: Establish train, test split
    X_train, X_test, Y_train, Y_test = train_test_split(tweetframe[feature_columns].copy(),
                                                        tweetframe['popularity'].copy(),
                                                        stratify = tweetframe['popularity'].copy(),
                                                        test_size=.2,
                                                        random_state=407,
                                                        shuffle=True)
    # Step 3: Scale the data
    sc = StandardScaler()
    X_train = sc.fit_transform(X_train)
    X_test = sc.fit_transform(X_test)

    # Step 3: Establish model
    ada = AdaBoostClassifier(dfc(max_depth=30))
    ada.fit(X_train, Y_train)
    Y_pred = ada.predict(X_test)

    # Step 4: Check model validity
    conf_matrix = confusion_matrix(Y_test, Y_pred)
    class_report = classification_report(Y_test, Y_pred)
    accuracy = accuracy_score(Y_test, Y_pred)

    return class_report, accuracy, [feature_columns, ada.feature_importances_]

class_report_random, accuracy_random, vec_random = random_forest(tweetframe, 25)
class_report_adaboost, accuracy_adaboost, vec_adaboost = adaboost_decision_tree(tweetframe, 25)

print('The Random Forest class report is: \n', class_report_random)
print('The Adaboost Decision Tree class report is: \n', class_report_adaboost)

print('The Random Forest accuracy score is:', accuracy_random)
print('The Adaboost Decision Tree accuracy score is: ', accuracy_adaboost)

a1 = len(tweetframe.retweet_count.loc[tweetframe['like_count'] < 25])
a2 = len(tweetframe.retweet_count)
print('The baseline accuracy is: ', float(a1) / float(a2))
