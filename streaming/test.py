import tweepy
import json
from os import chdir
from streaming.twitter_kafka_consumer import TwitterKafkaConsumer
from streaming.twitter_kafka_producer import TwitterKafkaProducer

chdir("../")
with open('config.json') as config_data:
    config = json.load(config_data)
auth = tweepy.OAuthHandler(config['consumer_key'], config['consumer_secret'])

access_token = config["access_token"]
access_token_secret = config["access_token_secret"]

consumer = TwitterKafkaConsumer(sid="test")
consumer.listen()
producer = TwitterKafkaProducer(access_token=access_token,
                                access_token_secret=access_token_secret,
                                sid="test")
producer.start()
consumer.await_termination()
