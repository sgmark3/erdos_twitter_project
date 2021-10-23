from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer as SIA
import pandas as pd

analyser = SIA()


def vader_tweet_sentiment(tweetframe):
    """
    This function computes the sentiment scores for a dataframe
    with pre-processed tweets
    :param tweetframe: dataframe with text info
    :return: A data frame with sentiment scores added
    """
    scores = []
    # Declaring the variables used for scoring
    compound_list = []
    positive_list = []
    negative_list = []
    neutral_list = []

    # Get the compound positive, neutral, and negative sentiment
    # scores for the tweet dataframe
    for i in range(tweetframe['text'].shape[0]):
        compound = analyser.polarity_scores(tweetframe['text'][i])['compound']
        pos = analyser.polarity_scores(tweetframe['text'][i])['pos']
        neu = analyser.polarity_scores(tweetframe['text'][i])['neu']
        neg = analyser.polarity_scores(tweetframe['text'][i])['neg']
        scores.append({"Compound_vader": compound,
                       "Positive_vader": pos,
                       "Negative_vader": neg,
                       "Neutral_vader": neu})
    # Convert the Vader sentiment scores into a dataframe
    sentiment_scores = pd.DataFrame.from_dict(scores)
    tweetframe = tweetframe.join(sentiment_scores)
    return tweetframe
