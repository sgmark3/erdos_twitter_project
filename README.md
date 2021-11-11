# Machine learning pipeline to extract a functional relationship between tweets and a stock's subsequent market reaction

# Team Members:
- [Jose A. Fortou](https://www.linkedin.com/in/jose-a-fortou-01957b214/)
- [Jithin Madhusudanan Sreekala](https://www.linkedin.com/in/jithinms)
- [Shashank Markande](https://www.linkedin.com/in/smarkande)
- [Andrew McMillan](https://www.linkedin.com/in/andrew-mcmillan-68983b96)
- [Yossathorn (Josh) Tawabutr](https://www.linkedin.com/in/yossathorn-tawabutr)

# Introduction and Motivation
This Github repository is devoted to completing the Erdos Institute, data science bootcamp project to obtain a certificate of competence and excellence in the techniques of data science and more specifically machine learning techniques. 

Our project stems from the corporate sponsored [Susquehanna](https://sig.com/) project which challenges participants to develop a machine learning framework to predict tweet popularity. We have chosen to build on the prompt by extending our project into a financial context. 

The first direction is to do just as the prompt suggests, so we collect Twitter data from various sources and attempt to predict the popularity of tweets based on various features that are exclusive to twitter, such as a user's number of followers, number of historic tweets, length of the tweet, etc., and we pair these features with those generated via natural language processing and libraries of historically positive and negative words in order to establish the sentiment of a tweet. 

The second direction is to then predict the movement of asset prices while conditioning on the results of the predicted tweet popularity. That is, we hypothesize that market movements will generally be affected by tweets that receive widespread attention, and by using the predicted tweets as initial data, we can potentially gain a first mover advantage in the market. 
# Data Gathering

### Dataset Description
