#Directional indicators
    # a. posWordsHe = word counts of positive words from Henry '08 (File already uploaded AM)
    # b. negWordsHe = word counts of negative words from Henry '08 (File already uploaded AM)
    # c. posWordsLM = word counts of positive words from Loughran and McDonald '11 (Still needed)
    # d. negWordsLM = word counts of negative words from Loughran and McDonald '11 (Still needed)
    # e. posNgrams = word counts of positive ngrams from Hagenau '13 (Still needed)
    # d. negNgrams = word counts of negative ngrams from Hagenau '13 (Still needed)


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
    
    def get_keybigrams(filename: str):
    """
    Input: 
    filename -> The file name and its directory in string, with ending included. 
                The directory must be relative to the location of this notebook.
                This file contains key bigrams separated by "\n". 
    
    This function should work for any n-grams, given that the text file is written in the same format.
                
    Output: 
    keybigrams_lemm -> The list of strings, each of which is a lemmatized bigram from the csv file.
    """
    # Load the file into a string
    text = open(filename, 'r').read()
    
    # Define keywords
    keybigrams = []
    
    # This is to keep track of the word we are reading as we traverse text.
    this_bigram = ""
    
    # Traversing text
    for i in range(len(text)):
        if text[i] == "\n":    # When running into "\n", we have finished reading a bigram.
            keybigrams.append(this_bigram)
            this_bigram = ""
        else:     # With an additional letter or space, just add it to the current bigram.
            this_bigram = this_bigram + text[i].lower()
    
    # If the string does not end in "\n", we will need to append the last bigram to keybigrams.
    if this_bigram != "":
        keybigrams.append(this_bigram)
    
    # Lemmatize keybigrams. See the function below.
    keybigrams_lemm_rept = key_lemmatize(keybigrams)
    
    # keybigrams_lemm_rept likely contains repeated elements. Eliminate them.
    keybigrams_lemm = list(set(keybigrams_lemm_rept))
    
    return keybigrams_lemm
