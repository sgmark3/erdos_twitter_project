#Directional indicators
    # a. posWordsHe = word counts of positive words from Henry '08
    # b. negWordsHe = word counts of negative words from Henry '08
    # c. posWordsLM = word counts of positive words from Loughran and McDonald '11
    # d. negWordsLM = word counts of negative words from Loughran and McDonald '11
    # e. posNgrams = word counts of positive ngrams from Hagenau '13
    # d. negNgrams = word counts of negative ngrams from Hagenau '13


class twitter_sentiment_directional_indicators:
    """
    This class computes the positive and negative sentiments associated with
    tweet data taken as input for the directional indicators. The scoring is 
    performed using the libraries of Henry '08, Loughran and McDonald '11, 
    and Hagenau '13.
    """

    def __init__(self, tweet_frame, pos_words, neg_words):
        self.tweet_frame = tweet_frame
        self.pos_words = pos_words
        self.neg_words = neg_words


    def pos_neg_counter(self, pos_library_name, neg_library_name):
         """
          This function  computes the number of positive and negative words, for a 
          given library, across all tweets and stores the counts in two new columns.
          
          param pos_library_name: The name in the literature for the positive library
          param neg_library_name: The name in the literature for the negative library
          return: The twitter dataframe with columns augmented with 
          positive and negative scores
         """
        
        if not isinstance(pos_library_name, str) or not isinstance(neg_library_name, str):
            print('The library names need to be strings.')
            return
        try:
            self.tweet_frame[pos_library_name], self.tweet_frame[neg_library_name] = self.tweet_frame['tweet'].apply(
                self.get_word_counts, args=
                (self.pos_words, self.neg_words,))
        except:
            print('Positive and Negative words not loaded correctly')
        return self.tweet_frame


    def get_word_counts(text,self):
        """
        This function counts the number of positive and negative
        words in a given text. 
        
        param self.pos_words: The collection of positive words
        param self.neg_words: The collection of negative words
        param text: The text to be analyzed
        """
        count_pos = 0
        count_neg = 0
        if not isinstance(self.pos_words, list) or not isinstance(self.neg_words, list):
            print('The positive and negative words are not in list format.')
            return

        for word in text:
            if word in self.pos_words:
                count_pos += 1
            if word in self.neg_words:
                count_neg += 1
        return [count_pos, count_neg]
