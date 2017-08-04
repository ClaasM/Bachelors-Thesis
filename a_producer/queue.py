import json
import time
import tweepy
from pyspark import SparkContext
from pyspark.streaming import StreamingContext


class TwitterStreamListener():
    def __init__(self):
        sc = SparkContext(appName="PythonStreamingQueueStream")
        ssc = StreamingContext(sc, 1)

        # Instantiate the twitter_stream

        # Get RDD queue of the streams json or parsed

        def get_next_tweet(self, twitter_stream):
            stream = twitter_stream.statuses.sample(block=True)
            tweet_in = None
            while not tweet_in or 'delete' in tweet_in:
                tweet_in = stream.next()
            return json.dumps()

        rdd_queue = []
        for i in range(3):
            rdd_queue += [ssc.sparkContext.parallelize([get_next_tweet("twitter_stream")], 5)]
        lines = ssc.queueStream(rdd_queue)
        lines.pprint()
        ssc.start()
        time.sleep(2)
        ssc.stop(stopSparkContext=True, stopGraceFully=True)
        # twitter_stream.filter(track=['iphone'], async=True)
