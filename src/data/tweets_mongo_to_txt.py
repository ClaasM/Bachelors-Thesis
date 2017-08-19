# Get 10k tweets and write them to a file for LDA training
from pymongo import MongoClient
import time

t0 = time.time()

tweet_cursor = MongoClient()['thesis-dev']['tweets'].aggregate([])
file = open("../../data/processed/tweets_text.txt", "w")

print("Done sampling")

count = 0
for tweet in tweet_cursor:
    if 'text' in tweet and tweet['text'] and 'lang' in tweet and tweet['lang'] == 'en':
        count += 1
        # print(count)
        file.write(repr(tweet['text']) + "\n")

print("Done writing")

file.close()

print(str(time.time() - t0))
