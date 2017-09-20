"""
Takes the tweets from the DB and puts them into the same format as the Sanders dataset
(With "N/A" for nonexistent information)
This makes the two datasets easily interchangeable in code
"""

from pymongo import MongoClient
import csv

tweet_cursor = MongoClient()['thesis-dev']['tweets'].aggregate([])
file = open("../../data/interim/stream_en.csv", "w")
writer = csv.writer(file)

for tweet in tweet_cursor:
    if 'text' in tweet and 'lang' in tweet and tweet['lang'] == 'en':
        writer.writerow(["N/A", "N/A", tweet['id'], tweet['text']])

file.close()
from sklearn.decomposition import NMF