import pandas as pd

local_path = '/Users/user/Desktop/Untitled/'
df = pd.read_csv(local_path + 'combined.csv')
henry_pos = open(local_path+'Henry08_poswords.txt', 'r')
henry_neg = open(local_path+'Henry08_negwords.txt', 'r')

henry_pos_set = set(henry_pos.read().split())
henry_neg_set = set(henry_pos.read().split())

# LM pos, LM neg
LM_pos = open(local_path + 'LM11_neg_words.txt', 'r')
LM_neg = open(local_path + 'LM11_pos_words.txt', 'r')

LM_pos_set = set(LM_pos.read().split())
LM_neg_set = set(LM_neg.read().split())

# ML pos, ML neg
ML_pos = pd.read_csv(local_path+'ML_positive_bigram.csv').iloc[:,0].to_list()
ML_neg = pd.read_csv(local_path+'ML_negative_bigram.csv').iloc[:,0].to_list()

ML_pos_set = set(ML_pos)
ML_neg_set = set(ML_neg)

#Aggregate sets into one

Aggregated = henry_pos_set.union(henry_neg_set,LM_pos_set, LM_neg_set,
        ML_pos_set, ML_neg_set)
#Aggregated = henry_pos_set.union(henry_neg_set)

df_filtered = df[df['text'].apply(lambda x: len(set(x.split()).intersection(Aggregated)) >= 1)]
print(df.shape, df_filtered.shape)
df_filtered.to_csv('filtered_data_v2.csv')

