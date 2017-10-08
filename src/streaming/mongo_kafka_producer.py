import json
import time

from kafka import KafkaProducer
from kafka.errors import NoBrokersAvailable
from pymongo import MongoClient as MCli


class MongoKafkaProducer(object):
    """
    Used for testing purposes
    """

    def __init__(self):
        conn = {'host': 'localhost', 'ip': '27017'}
        self.client = MCli(**conn)
        self.db = self.client['twitter-dev']

        try:
            self.producer = KafkaProducer(bootstrap_servers='docker:9092')
        except NoBrokersAvailable:
            print("Kafka Server not started!")
            raise

    def update(self):
        cursor = self.db['tweets'].find()
        for tweet in cursor:
            self.producer.send(tweet)
            time.sleep(.1)  # send around 10 tweets a second
        print("All tweets sent")
        self.stop()

    def stop(self):
        self.producer.close(timeout=10)
        print("Kafka producer closed")
