
import numpy as np
import matplotlib.pyplot as plt

from sklearn.metrics import f1_score
from sklearn.metrics import classification_report, confusion_matrix, accuracy_score
from sklearn.naive_bayes import GaussianNB, BernoulliNB
import seaborn as sns
from sklearn import metrics

def get_NaiveBayes(X_train, X_test, y_train, y_test):

    naiveBayes = GaussianNB()
    naiveBayes.fit(X_train, y_train)
    predictions  = naiveBayes.predict(X_test)


    print('________________ GaussianNB ________________')
    class_report = classification_report(y_test, predictions)
    accuracy = accuracy_score(y_test, predictions)

    print ('report :', class_report)
    print('accuracy :',accuracy)
    print('f1_score ', f1_score(y_test, predictions, average='weighted'))
    print('f1_score ', f1_score(y_test, predictions, average='weighted'))
    
    cm = metrics.confusion_matrix(y_test, predictions)
    print(cm)
    plt.figure(figsize=(9,9))
    sns.heatmap(cm, annot=True, fmt=".3f", linewidths=.5, square = True, cmap = 'Blues_r');
    plt.ylabel('Actual label');
    plt.xlabel('Predicted label');
    all_sample_title = 'Accuracy Score: {0} %'.format(round(accuracy*100, 2))
    plt.title(all_sample_title, size = 15)
    plt.show()
    
def get_MultinomialNB(X_train, X_test, y_train, y_test):
    naiveBayes = BernoulliNB()
    naiveBayes.fit(X_train, y_train)
    predictions  = naiveBayes.predict(X_test)

    print('________________ BernoulliNB ________________')
    class_report = classification_report(y_test, predictions)
    accuracy = accuracy_score(y_test, predictions)

    print ('report :', class_report)
    print('accuracy :',accuracy)
    print('f1_score ', f1_score(y_test, predictions, average='weighted'))
    cm = metrics.confusion_matrix(y_test, predictions)
    print(cm)
    plt.figure(figsize=(9,9))
    sns.heatmap(cm, annot=True, fmt=".3f", linewidths=.5, square = True, cmap = 'Blues_r');
    plt.ylabel('Actual label');
    plt.xlabel('Predicted label');
    all_sample_title = 'Accuracy Score: {0} %'.format(round(accuracy*100, 2))
    plt.title(all_sample_title, size = 15)
    plt.show()