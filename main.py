# Establish Sentiment Features
# 1. Directional indicators
# a. posWordsHe = word counts of positive words from Henry '08
# b. negWordsHe = word counts of negative words from Henry '08
# c. posWordsLM = word counts of positive words from Loughran and McDonald '11
# d. negWordsLM = word counts of negative words from Loughran and McDonald '11
# e. posNgrams = word counts of positive ngrams from Hagenau '13
# d. negNgrams = word counts of negative ngrams from Hagenau '13
# Train_test split


class Twitter_Sentiment_Analysis:
    """
    This class computes the positive and negative sentiments associated with
    tweet data taken as input. The scoring is performed using the libraries of
    Henry '08, Loughran and McDonald '11, and Hagenau '13.
    """

    def __init__(self, tweet_frame, pos_words, neg_words):
        self.tweet_frame = tweet_frame
        self.pos_words = pos_words
        self.neg_words = neg_words


def pos_neg_counter(self, pos_library_name, neg_library_name):
    if not isinstance(pos_library_name, str) or not isinstance(neg_library_name, str):
        print('The library names need to be strings.')
    try:
        self.tweet_frame[pos_library_name], self.tweet_frame[neg_library_name] = self.tweet_frame['tweet'].apply(
            get_word_counts, args=
            (self.pos_words, self.neg_words,))
    except:
        print('Positive and Negative words not loaded correctly')


def get_word_counts(text, pos_words, neg_words):
    count_pos = 0
    count_neg = 0
    if not isinstance(pos_words, list) or not isinstance(neg_words, list):
        print('The positive and negative words are not in list format.')

    for word in text:
        if word in pos_words:
            count_pos += 1
        if word in neg_words:
            count_neg += 1
    return [count_pos, count_neg]
