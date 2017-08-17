# Get 10k tweets and write them to a file for LDA training
from pymongo import MongoClient
import time

t0 = time.time()

tweet_cursor = MongoClient()['twitter-dev']['tweets'].aggregate([{"$sample": {"size": 10000}}])
file = open("../../data/processed/tweets_text.txt", "w")

print("Done sampling")

for tweet in tweet_cursor:
    if 'text' in tweet and tweet['text'] and 'lang' in tweet and tweet['lang'] == 'en':
        file.write(repr(tweet['text']) + "\n")

print("Done writing")

file.close()

print(str(time.time() - t0))
