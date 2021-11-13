import pandas as pd
from csv import reader

directory = "Twitter_Sentiment_Analysis/Directional_Feature_Libraries/"

words1 = []
with open('Twitter_Sentiment_Analysis\Directional_Feature_Libraries\Henry08_negwords.txt') as f1:
    words1 = f1.readline().strip().split()
    
words2 = []
with open('Twitter_Sentiment_Analysis\Directional_Feature_Libraries\Henry08_poswords.txt') as f1:
    words2 = f1.readline().strip().split()
    

words3 = []
with open("Twitter_Sentiment_Analysis\Directional_Feature_Libraries\LM11_neg_words.txt") as f2:
    words3 = f2.readline().strip().split()
    
words4 = []
with open("Twitter_Sentiment_Analysis\Directional_Feature_Libraries\LM11_pos_words.txt") as f2:
    words4 = f2.readline().strip().split()

result = []

for w in [words1, words2, words3, words4]:
    result += list(map(lambda x: x.lower(), w  )) 

result = list(set(result))
print(len(words1), len(words2) , len(words3), len(words4))

words_result = result[::]

with open("Twitter_Sentiment_Analysis\Directional_Feature_Libraries\ML_negative_bigram.csv", 'r') as read_obj:
    # pass the file object to reader() to get the reader object
    csv_reader = reader(read_obj)
    # Iterate over each row in the csv using reader object
    for row in csv_reader:
        # row variable is a list that represents a row in csv
        result += row

with open("Twitter_Sentiment_Analysis\Directional_Feature_Libraries\ML_positive_bigram.csv", 'r') as read_obj:
    # pass the file object to reader() to get the reader object
    csv_reader = reader(read_obj)
    # Iterate over each row in the csv using reader object
    for row in csv_reader:
        # row variable is a list that represents a row in csv
        result += row

print()
print(len(set(result)))
print(len(result) - len(words_result))

# check this 
# https://developer.twitter.com/en/docs/twitter-api/enterprise/search-api/overview
