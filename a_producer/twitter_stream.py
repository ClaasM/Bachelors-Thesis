import json

import tweepy
from dashboard import socketio  # from kafka import KafkaProducer


class TwitterStreamListener(tweepy.StreamListener):
    def __init__(self, access_token, access_token_secret, sid):
        self.sid = sid
        with open('config.json') as config_data:
            config = json.load(config_data)
        auth = tweepy.OAuthHandler(config['consumer_key'], config['consumer_secret'])
        auth.set_access_token(access_token, access_token_secret)
        api = tweepy.API(auth)
        twitter_stream = tweepy.Stream(auth=api.auth, listener=self)
        # TODO
        twitter_stream.filter(track=['iphone'], async=True)

    def on_data(self, data):
        # TODO continue by emitting only to session id here
        socketio.emit('dashboard.update', data=json.loads(data), room=self.sid)


def on_error(self, status_code):
    if status_code == 420:
        return False
