
import streamlit as st
from PIL import Image
image_heatmap = Image.open('web_app/images/correalation_heatmap.png')
image_users = Image.open('web_app/images/save_twitter_2.png')
image_textlength = Image.open('web_app/images/text_length.png')
image_vader = Image.open('web_app/images/vader.png')
image_hourly_distribution = Image.open('web_app/images/hourly_distribution.png')

def app():
    st.title(' Tweet popularity ')

    st.markdown('''
    # Data Gathering

    We gather historic data from both Twitter and the stock market using the [Twitter API](https://developer.twitter.com/en/docs) and the [AlphaVantage API](https://www.alphavantage.co/), respectively. The descriptions of both data sets can be found below.

    ## Twitter Dataset Description

    For the historic twitter data, we query the Twitter API for tweets from financially relevant Twitter accounts, such as Bloomberg, Yahoo Finance, The Economist, etc. from October 2019 to October 2021, and we filter the tweets for those that include either a company's full name, a hashtag of a company's stock ticker, or a cash tag of a company's stock ticker. The Twitter data was only pulled for those companies that are in the SP500 list, but our code could easily be generalized to include any or all companies that exist on any stock exchange.
    ''')
    st.image(image_users, caption='Twitter user accounts used in the project')
    st.markdown('''
    We chose the above two-step filtering procedure (filtering via Twitter account and company mentions) due to the generally known, widespread presence of noise on Twitter. Surprisingly over the course of this project, we discovered that including simply the latter failed to sufficiently filter out noise, even when paired with additional filters such as the presence of financially relevant words. The result of our two-step filtering is that we recover Tweet data that is financially contextualized, and hence, we expect these tweets to serve as strong signals in predicting future market movement. Admittedly, this filtering procedure does forego other potentially strong signals such as a celebrity tweeting about a particular company or a given company tweeting about the release of a new project; the inclusion of such data is a potential direction for future work.
    
The raw Twitter data that we pull has the following attributes:

* The tweet text
* The mentions in a tweet
* The number of followers for the poster of the tweet
* The number of followings for the poster of the tweet
* The location of the the user
* The tweet's time stamp
* The tweet's hashtags and cashtags
* The URLs that appear in the tweet
* The number of likes, quotes, replies, and retweets of the tweet
* The tweet's listed count

In the data pre-processing section below, we detail which of these data attributes were kept and which were transformed or processed into a more useable way.

## Stock Dataset Description

For the historic stock data, we query the Alphavantage API for stock data pertaining to SP500 companies from March 2019 to March 2021. The time resolution of the stock prices is minute to minute. As twitter is a comparitively high frequency social media platform, we insisted on retaining minute to minute data, but unfortunately, this time resolution was only freely available over the aforementioned period. More extensive data for the purposes of backtesting can be obtained, albeit at substantial cost, via data repository sites such as [QuantQuote](https://quantquote.com/). We retain most of the standard asset data such as opening price, closing price, trading volume, 52 week high and lows.

# Data Pre-processing and Visualization

In order to make our data accessible via the machine learning algorithms of SKlearn, we first clean the data for anomalies and convert un-interpretable data into numerical values. That is, we convert the following Twitter data into simply a count of the number of each such occurence:

* URLs appearing in a tweet
* Hashtags appearing in a tweet
* Cashtags appearing in a tweet
* Other entities appearing in a tweet
* News agencies appearing in a tweet
    ''')
    st.image(image_heatmap, caption="Correlation heat map of tweets features")
    st.markdown('''
For example, if there are two URLs that appear in a tweet, then we replace the column corresponding to the URLs with a count of two.

We are also concerned with the effects that a tweet's sentiment has on its popularity, we employ two metrics to determine tweet sentiment. The first is the use of the [Vader](https://github.com/cjhutto/vaderSentiment) natural language processing library. Vader has an advantage over other language processing libraries, because it is specifically designed to characterize the sentiment of social media data. That is, it incorporates slang terms, acronyms, and emojis- all of which are commonplace on social media. Secondly, we employ a word count of several word and bigram libraries that have appeared in the financial literature to characterize whether a tweet speaks positively or negatively about the underlying company or the companies' stock. The libraries that we use can be found at [(Henry, 2008)](https://journals.sagepub.com/doi/10.1177/0021943608319388), [(Loughran and Mcdonald, 2011)](https://onlinelibrary.wiley.com/doi/10.1111/j.1540-6261.2010.01625.x), and [(Hagenau, 2013)](https://www.researchgate.net/publication/254051649_Automated_News_Reading_Stock_Price_Prediction_Based_on_Financial_News_Using_Context-Specific_Features).
''')
    st.image(image_vader, caption='Vader sentiment analysis')
    st.markdown('''
Finally, as the tweet prediction literature often explicitly employs time stamps, we  make three additional columns - morning, afternoon, and night that are derived from the the time stamp associated to when the tweet was made.

To gain a general sense for the relationships between each column of Twitter data, we have performed a preliminary, data visualization, which can be found in the
[Data_Visualization](https://github.com/msjithin/erdos_twitter_project/tree/main/Data_Visualization) directory of this Github repository.


    ''')
    st.image(image_textlength, caption='Text character count')
    st.image(image_hourly_distribution, caption='Hourly distribution of likes in 24 hours')
    
