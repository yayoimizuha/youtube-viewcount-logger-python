import datetime
import os
import pprint

import tweepy

consumer_key = os.environ['API_KEY']
consumer_secret = os.environ['API_SECRET']
access_token = os.environ['ACCESS_TOKEN']
access_token_secret = os.environ['ACCESS_TOKEN_SECRET']

auth = tweepy.OAuth1UserHandler(
    consumer_key=consumer_key,
    consumer_secret=consumer_secret,
    access_token=access_token,
    access_token_secret=access_token_secret
)

api = tweepy.API(auth)


def tweet(text=None):
    if text is None:
        text = "test tweet.\n" + str(datetime.datetime.now())
    response = api.update_status(text)
    pprint.pprint(response)
