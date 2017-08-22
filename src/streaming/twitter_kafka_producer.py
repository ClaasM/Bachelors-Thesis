import json
import os

import tweepy
from kafka import KafkaProducer
from kafka.errors import NoBrokersAvailable


# TODO test & figure out tweepy's twitter_stream.sitestream, .userstream, .retweet

class TwitterKafkaProducer(tweepy.StreamListener):
    """
    Listens on the Twitter stream and sends all events to the Kafka queue.
    The the topic is the session id which identifies the client.
    """

    def __init__(self, access_token, access_token_secret, sid):
        # Create the twitter stream
        super().__init__()
        self.sid = sid
        dir_path = os.path.dirname(os.path.realpath(__file__))
        with open(dir_path + '/../../config.json') as config_data:
            config = json.load(config_data)
        auth = tweepy.OAuthHandler(config['consumer_key'], config['consumer_secret'])
        auth.set_access_token(access_token, access_token_secret)
        self.api = tweepy.API(auth)
        try:
            self.producer = KafkaProducer(bootstrap_servers='docker:9092')
        except NoBrokersAvailable:
            print("Kafka Server not started!")
            raise
            # TODO handle appropriately
        self.twitter_stream = tweepy.Stream(auth=self.api.auth, listener=self)

    def update(self, settings):
        # Stop the current stream if there is one
        self.twitter_stream.disconnect()

        # Start the new stream with new settings
        stream_type = settings['type']
        del settings['type']
        del settings['filter_level']  # TODO find a way to be able to use unicode --> Make a tweepy3 fork maybe?
        if stream_type == 'site':
            self.twitter_stream.sitestream(**settings, async=True)
        elif stream_type == 'user':
            self.twitter_stream.userstream(**settings, async=True)
        elif stream_type == 'sample':
            self.twitter_stream.sample(**settings, async=True)
        elif stream_type == 'public':
            self.twitter_stream.filter(**settings, async=True)
        elif stream_type == 'retweet':
            self.twitter_stream.retweet(async=True)
        elif stream_type == 'firehose':
            self.twitter_stream.firehose(**settings, async=True)
        else:
            raise "Unknown type: " + stream_type

    def stop(self):
        self.twitter_stream.disconnect()
        print("Disconnected from Twitter stream")
        self.producer.close(timeout=10)
        print("Kafka producer closed")

    def on_status(self, status):
        """Called when a new status arrives"""
        self.producer.send(str(self.sid), json.dumps(status._json).encode('utf-8'))
        self.producer.flush()  # TODO probably don't need to always do that
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
