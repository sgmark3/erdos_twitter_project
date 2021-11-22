import pandas as pd
import spacy

#from vader_tweet_sentiment import vader_tweet_sentiment

from Twitter_Sentiment_Analysis.vader_tweet_sentiment import vader_tweet_sentiment
nlp = spacy.load('en_core_web_sm')

# # Customize there two lines
# librarypath = ".../GitHub/erdos_twitter_project"
# githubpath = ".../GitHub/erdos_twitter_project/Data_Preprocessed/"
librarypath = 'Twitter_Sentiment_Analysis'

def get_text_analysis(df_tweets):
    """
    This function downloads the tweet csv file into a dataframe,
    compute the Vader scores and normalized word counts based on all libraries,
    remove rows without non-neutral sentiments,
    (0 in everything except neutral Vader score of 1)
    and finally delete the text column. 
    The resulting data frame is then saved to the GitHub directory.
    """
    keyfiles_words = [librarypath + "/Directional_Feature_Libraries/Henry08_poswords.txt",
                      librarypath + "/Directional_Feature_Libraries/Henry08_negwords.txt",
                      librarypath + "/Directional_Feature_Libraries/LM11_pos_words.txt",
                      librarypath + "/Directional_Feature_Libraries/LM11_neg_words.txt"]
    keyfiles_bigrams = [librarypath + "/Directional_Feature_Libraries/ML_positive_bigram.csv",
                        librarypath + "/Directional_Feature_Libraries/ML_negative_bigram.csv"]
    keyfiles_news = [librarypath + "/Relevance_Feature_Libraries/news_library.txt"]
    keys = [get_news_agencies(keyfile) for keyfile in keyfiles_news] + [get_keywords(keyfile) for keyfile in keyfiles_words] + [get_keybigrams(keyfile) for keyfile in keyfiles_bigrams]
    key_library = ["News_agencies", "Henry08_pos", "Henry08_neg", "LM11_pos", "LM11_neg", "Hagenau13_pos", "Hagenau13_neg"]
    wordcounts_all = [[-1 for i in range(df_tweets.shape[0])] for j in range(len(keys) + 2)]
    for i in range(df_tweets.shape[0]):
        wordcounts = tweet_to_wordcounts(df_tweets["text"].iloc[i], keys)
        for j in range(len(keys) + 2):
            wordcounts_all[j][i] = wordcounts[j]
    for j in range(len(keys)):
        df_tweets["Word_count_" + key_library[j]] = wordcounts_all[j]
    df_tweets["Tweet_Length_characters"] = wordcounts_all[-2]
    df_tweets["Tweet_Length_words"] = wordcounts_all[-1]
    df_tweets = vader_tweet_sentiment(df_tweets)
    #df_tweets.to_parquet(githubpath + "df_" + company_name + "_features_added.parquet", index=False)
    return df_tweets

  
def get_keywords(filename: str):
    """
    Input: 
    filename -> The file name and its directory in string, with ending included. 
                The directory must be relative to the location of this notebook.
                This file contains keywords separated by space.
                
    Output: 
    keywords -> The set of strings, each of which is a word from the txt file.
    """
    text = open(filename, 'r').read()
    keywords = []
    this_word = ""
    for i in range(len(text)):
        if text[i] == " ":    
            keywords.append(this_word)
            this_word = ""
        elif text[i:] == "\n":   
            break
        else:     
            this_word = this_word + text[i].lower()
    if this_word != "":
        keywords.append(this_word)
    return set(keywords)

  
def get_keybigrams(filename: str):
    """
    Input: 
    filename -> The file name and its directory in string, with ending included. 
                The directory must be relative to the location of this notebook.
                This file contains key bigrams separated by "\n". 
    
    This function should work for any n-grams, given that the text file is written in the same format.
                
    Output: 
    keybigrams_lemm -> The set of strings, each of which is a bigram from the csv file.
    """
    text = open(filename, 'r').read()
    keybigrams = []
    this_bigram = ""
    for i in range(len(text)):
        if text[i] == "\n":   
            keybigrams.append(this_bigram)
            this_bigram = ""
        else:    
            this_bigram = this_bigram + text[i].lower()
    if this_bigram != "":
        keybigrams.append(this_bigram)
    return set(keybigrams)

def get_news_agencies(filename: str):
    """
    Input: 
    filename -> The file name and its directory in string, with ending included. 
                The directory must be relative to the location of this notebook.
                This file contains names of news agencies separated by space.
                
    Output: 
    news_agencies -> The set of strings, each of which is a name of news agency from the input file.
    """
    text = open(filename, 'r').read()
    news_agencies = []
    this_word = ""
    for i in range(len(text)):
        if text[i] == " ":   
            news_agencies.append(this_word)
            this_word = ""
        elif text[i:] == "\n":   
            break
        else:     
            this_word = this_word + text[i].lower()
    if this_word != "":
        news_agencies.append(this_word)
    return set(news_agencies)


def tweet_to_wordcounts(tweet, keys):
    """
    Input:
    tweet -> The raw tweet text in string
    keys -> The list of sets of key words. For example, keys = [henry08_pos, henry08_neg, ..., newslib]
            Each keyword is assumed to contain only English letter. WARNING: must remove bigrams
    normalize -> If True, the word count for each keyword list is normalized by tweet_length.
                 If False, the raw word count will be returned.
    
    Output:
    wordcounts -> A list of length num_keys. Each element is the word count corresponding
                  to the number of phrases from one of the phrase lists that appear in the tweet, 
                  as reported in wordlocs.
    """
    tweet_doc = nlp(tweet.lower())
    tweet_words = [token.text for token in tweet_doc if not token.is_stop]
    tweet_bigrams = set([tweet_words[i] + " " + tweet_words[i+1] for i in range(len(tweet_words) - 1)])
    wordcounts = []
    tweet_length = len(tweet)
    tweet_length_word = len(tweet_doc)
    for i in range(len(keys) - 2):
        tweet_words_set = set(tweet_words)
        this_wordcount = len(tweet_words_set.intersection(keys[i])) 
        wordcounts.append(this_wordcount)
    for i in range(2):
        this_wordcount = len(tweet_bigrams.intersection(keys[i-2]))
        wordcounts.append(this_wordcount)
    wordcounts.append(tweet_length)
    wordcounts.append(tweet_length_word)
    return wordcounts




  
  
