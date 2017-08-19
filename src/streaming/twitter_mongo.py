import json
import time

import tweepy
from kafka import KafkaProducer
from kafka.errors import NoBrokersAvailable
from pymongo import MongoClient as MCli


class TwitterMongo(tweepy.StreamListener):
    """
    Used for testing purposes
    """

    def __init__(self):
        # Initialize database connection
        self.coll = MCli()['thesis-dev']['tweets']

        # initialize streaming
        with open('../../config.json') as config_data:
            config = json.load(config_data)
        auth = tweepy.OAuthHandler(config['consumer_key'], config['consumer_secret'])
        # the sample endpoint is user context only
        auth.set_access_token(config['access_token'], config['access_token_secret'])
        self.api = tweepy.API(auth)
        self.twitter_stream = tweepy.Stream(auth=self.api.auth, listener=self)

        self.twitter_stream.sample(languages=['en'], async=True)

    """
    Listener Stuff
    """

    def on_status(self, status):
        """Called when a new status (tweet) arrives"""
        # save to db
        self.coll.insert(status._json)
        return

    def on_error(self, status_code):
        print(status_code)
        if status_code == 420:
            return False

    def on_connect(self):
        print("Connected to Twitter Stream!")

    def keep_alive(self):
        """Called when a keep-alive arrived"""
        print("keep_alive")
        return

    def on_exception(self, exception):
        """Called when an unhandled exception occurs."""
        print("on_exception")
        return

    def on_delete(self, status_id, user_id):
        """Called when a delete notice arrives for a status"""
        print("on_delete")
        return

    def on_event(self, status):
        """Called when a new event arrives"""
        print("on_event")
        # socketio.emit('dashboard.event-create', data=status._json, room=self.sid)
        return

    def on_direct_message(self, status):
        """Called when a new direct message arrives"""
        print("on_direct_message")
        # socketio.emit('dashboard.direct_message-create', data=status._json, room=self.sid)
        return

    def on_friends(self, friends):
        """Called when a friends list arrives.

        friends is a list that contains user_id
        """
        print("on_friends")
        # socketio.emit('dashboard.friends-create', data=json.loads(friends), room=self.sid)
        return

    def on_limit(self, track):
        """Called when a limitation notice arrives"""
        print("on_limit")
        return

    def on_timeout(self):
        """Called when stream connection times out"""
        print("on_timeout")
        return

    def on_disconnect(self, notice):
        """Called when twitter sends a disconnect notice

        Disconnect codes are listed here:
        https://dev.twitter.com/docs/streaming-apis/messages#Disconnect_messages_disconnect
        """
        print("on_disconnect")
        return

    def on_warning(self, notice):
        """Called when a disconnection warning message arrives"""
        print("on_warning")
        return
