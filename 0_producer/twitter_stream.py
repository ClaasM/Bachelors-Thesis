import json

import tweepy
from kafka import KafkaProducer


def initialize():
    with open('config.json') as config_data:
        config = json.load(config_data)

    auth = tweepy.OAuthHandler(config['consumer_key'], config['consumer_secret'])
    auth.set_access_token(config['access_token'], config['access_token_secret'])
    api = tweepy.API(auth)

    stream = TwitterStreamListener()
    twitter_stream = tweepy.Stream(auth=api.auth, listener=stream)
    twitter_stream.filter(track=['iphone'], async=True)


class TwitterStreamListener(tweepy.StreamListener):
    def __init__(self):
        self.producer = KafkaProducer(bootstrap_servers='docker:9092')
        self.tweets = []

    def on_data(self, data):
        data = json.loads(data)
        if u'text' not in data:
            print("Text not in data")
        else:
            text = json.dumps(data[u'text'])
            print(text)
            self.producer.send('iphone', json.dumps(text).encode('utf-8'))
            self.producer.flush()

    def on_error(self, status_code):
        if status_code == 420:
            return False


if __name__ == "__main__":
    initialize()
