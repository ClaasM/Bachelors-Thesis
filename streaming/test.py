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

# Start the consumer first
consumer = TwitterKafkaConsumer(sid="test")
consumer.start()
# Then start the producer
producer = TwitterKafkaProducer(access_token=access_token,
                                access_token_secret=access_token_secret,
                                sid="test")
producer.start()





# This is only needed here because the script will terminate otherwise; do not use on the server because it blocks
consumer.await_termination()
