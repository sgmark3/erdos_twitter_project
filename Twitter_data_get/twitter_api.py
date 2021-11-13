from config import twitter_daq as tk
import tweepy


# Enter your own credentials obtained 
# from your developer account
"""
how keys are stored:
class twitter_daq:
        APP_ID = "XXXX"
        USER_AGENT = "twitter_daq_app"
        CONSUMER_KEY       ="XXXXXXXX"
        CONSUMER_SECRET    = "XXXXXXXX"
        ACCESS_TOKEN_KEY   = "XXXXXXXX"
        ACCESS_TOKEN_SECRET= "XXXXXXXX"
        BEARER_TOKEN       = "XXXXXXXX"
"""

auth = tweepy.OAuthHandler(tk.CONSUMER_KEY, tk.CONSUMER_SECRET)
auth.set_access_token(tk.ACCESS_TOKEN_KEY, tk.ACCESS_TOKEN_SECRET)
my_api = tweepy.API(auth)


def bearer_oauth(r):
    """
    Method required by bearer token authentication.
    """
    r.headers["Authorization"] = f"Bearer {tk.BEARER_TOKEN}"
    r.headers["User-Agent"] = tk.USER_AGENT
    return r
