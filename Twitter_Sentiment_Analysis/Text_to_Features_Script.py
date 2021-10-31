import pandas as pd
import spacy

from vader_tweet_sentiment import vader_tweet_sentiment

nlp = spacy.load('en_core_web_sm')

localpath = "/Users/josht/Documents/Tweets_raw/"
librarypath = "/Users/josht/Documents/GitHub/erdos_twitter_project"
githubpath = "/Users/josht/Documents/GitHub/erdos_twitter_project/Data_Preprocessed/"

def main(filename):
    """
    This function downloads the tweet csv file into a dataframe,
    compute the Vader scores and normalized word counts based on all libraries,
    remove rows without non-neutral sentiments,
    (0 in everything except neutral Vader score of 1)
    and finally delete the text column. 
    The resulting data frame is then saved to the GitHub directory.
    """
    csv_directory = localpath + filename
    company_name = filename[3:-4]         # Assuming raw file name "df_NameOfCompany.csv"
    df_tweets = pd.read_csv(csv_directory)
    keyfiles_words = [librarypath + "/Twitter_Sentiment_Analysis/Directional_Feature_Libraries/Henry08_poswords.txt",
                      librarypath + "/Twitter_Sentiment_Analysis/Directional_Feature_Libraries/Henry08_negwords.txt",
                      librarypath + "/Twitter_Sentiment_Analysis/Directional_Feature_Libraries/LM11_pos_words.txt",
                      librarypath + "/Twitter_Sentiment_Analysis/Directional_Feature_Libraries/LM11_neg_words.txt"]
    keyfiles_bigrams = [librarypath + "/Twitter_Sentiment_Analysis/Directional_Feature_Libraries/ML_positive_bigram.csv",
                        librarypath + "/Twitter_Sentiment_Analysis/Directional_Feature_Libraries/ML_negative_bigram.csv"]
    keyfiles_news = [librarypath + "/Twitter_Sentiment_Analysis/Relevance_Feature_Libraries/news_library.txt"]
    keys = [get_keywords(keyfile) for keyfile in keyfiles_words] + [get_keybigrams(keyfile) for keyfile in keyfiles_bigrams] + [get_news_agencies(keyfile) for keyfile in keyfiles_news]
    key_library = ["Henry08_pos", "Henry08_neg", "LM11_pos", "LM11_neg", "Hagenau13_pos", "Hagenau13_neg", "News_agencies"]
    wordcounts_all = [[-1 for i in range(df_tweets.shape[0])] for j in range(len(keys))]
    for i in range(df_tweets.shape[0]):
      wordcounts = tweet_to_wordcounts(df_tweets["text"].iloc[i], keys[:4] + [keys[-1]])
      bigramcounts = tweet_to_bigramcounts(df_tweets["text"].iloc[i], keys[4:6])
      for j in range(len(keys)):
          if j <= 3:
              wordcounts_all[j][i] = wordcounts[j]
          elif j == len(keys) - 1:
              wordcounts_all[-1][i] = wordcounts[-1]
          else:
              wordcounts_all[j][i] = bigramcounts[j - 4]
    for j in range(len(keys[:-1])):
      df_tweets["Word_count_" + key_library[j]] = wordcounts_all[j]
    df_tweets["News_agencies_names_count"] = wordcounts_all[-1]
    df_tweets = vader_tweet_sentiment(df_tweets)
    df_trivial_tweets = df_tweets.loc[df_tweets["Word_count_Henry08_pos"] == 0].loc[df_tweets["Word_count_Henry08_neg"] == 0].loc[df_tweets["Word_count_LM11_pos"] == 0].loc[df_tweets["Word_count_LM11_neg"] == 0].loc[df_tweets["Word_count_Hagenau13_pos"] == 0].loc[df_tweets["Word_count_Hagenau13_neg"] == 0].loc[df_tweets["News_agencies_names_count"] == 0].loc[df_tweets["Compound_vader"] == 0].loc[df_tweets["Positive_vader"] == 0].loc[df_tweets["Negative_vader"] == 0].loc[df_tweets["Neutral_vader"] == 1]
    df_tweets_shorten = df_tweets.drop(df_trivial_tweets.index).copy()
    df_tweets_notext = df_tweets_shorten.drop(columns=["text"]).copy()
    df_tweets_notext.to_csv(githubpath + "/Data_Preprocessed/df_" + company_name + "_features_added.csv", index=False)
    print(company_name + "finished")                  # Comment out if prefer quiet

  
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


def tweet_to_wordcounts(tweet, keys, normalize=True):
    """
    Input:
    tweet -> The raw tweet text in string
    keys -> The list of sets of key words. For example, keys = [henry08_pos, henry08_neg, ..., newslib]
            Each keyword is assumed to contain only English letter. WARNING: must remove bigrams
    normalize -> If True, the word count for each keyword list is normalized by tweet_length.
                 If False, the raw word count will be returned.
    
    Output:
    wordcounts -> A list of length num_keys. Each element is the (normalized) word count corresponding
                  to the number of phrases from one of the phrase lists that appear in the tweet, 
                  as reported in wordlocs.
    """
    tweet_doc = nlp(tweet.lower())
    tweet_words = set([token.text for token in tweet_doc])
    wordcounts = []
    for i in range(len(keys)):    
        this_wordcount = len(tweet_words.intersection(keys[i])) 
        if normalize:
            this_wordcount_normalized = this_wordcount / len(tweet)
            wordcounts.append(this_wordcount_normalized)
        else:
            wordcounts.append(this_wordcount)
    return wordcounts


def tweet_to_bigramcounts(tweet, keys, normalize=True):
    """
    Input:
    tweet -> The raw tweet text in string
    keys -> The list of sets of key bigrams. For example, keys = ["Hagenau13_pos", "Hagenau13_neg"]
            Each key bigram is assumed to contain only English letter and space.
    normalize -> If True, the word count for each keyword list is normalized by tweet_length.
                 If False, the raw word count will be returned.
    
    Output:
    wordcounts -> A list of length num_keys. Each element is the (normalized) word count corresponding
                  to the number of phrases from one of the phrase lists that appear in the tweet, 
                  as reported in wordlocs.
    """
    tweet_doc = nlp(tweet.lower())
    tweet_words = [token.text for token in tweet_doc if not token.is_stop]
    tweet_bigrams = set([tweet_words[i] + " " + tweet_words[i+1] for i in range(len(tweet_words) - 1)])
    wordcounts = []
    for i in range(len(keys)):      
        this_wordcount = len(tweet_bigrams.intersection(keys[i])) 
        if normalize:
            this_wordcount_normalized = this_wordcount / len(tweet)
            wordcounts.append(this_wordcount_normalized)
        else:
            wordcounts.append(this_wordcount)
    return wordcounts
  
  
  
