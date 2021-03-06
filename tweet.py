import datetime
import glob
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


def tweet(text=None, name=None, raw=False):
    if raw is True:
        api.update_status(text)
        return
    if name is not None:
        images = glob.glob(os.path.join('images', name + '*.png'))
        print(name)
        print(images)
        media_ids = [api.media_upload(i).media_id_string for i in images]
        response = api.update_status(text, media_ids=media_ids)
        pprint.pprint(response)
        return

    if text is None:
        text = "test tweet.\n" + str(datetime.datetime.now()) + str(name)
    response = api.update_status(text)
    pprint.pprint(response)
