"""
This script
* Loads documents as aggregation of tweets stored in a MongoDB collection
* Cleans up the documents
* Creates a dictionary and corpus that can be used to train an LDA model
* Training of the LDA model is not included but follows:
  lda = models.LdaModel(corpus, id2word=dictionary, num_topics=100, passes=100)
Author: Alex Perrier
Python 2.7
TODO attributions https://github.com/alexperrier/datatalks/
"""

from collections import defaultdict
from gensim import corpora
from pymongo import MongoClient

from src.streaming import spark_functions

# connect to the MongoDB
db = MongoClient()['thesis-dev']

# Load tweets from db
# Filter out non-english tweets
documents = [tweet for tweet in db.tweets.find()
             if 'lang' in tweet and tweet['lang'] == 'en']

# Tokenize with the same tokenization function used during streaming
# This ensures consistent results
tokenizer = spark_functions.tokenize()
documents = [tokenizer(document) for document in documents]

# Remove words that only occur once
token_frequency = defaultdict(int)
# count all token
for doc in documents:
    for token in doc:
        token_frequency[token] += 1
# keep words that occur more than once
documents = [[token for token in doc if token_frequency[token] > 1]
             for doc in documents]

# Build a dictionary where for each document each word has its own id
dictionary = corpora.Dictionary(documents)
dictionary.compactify()
# and save the dictionary for future use
dictionary.save('../../data/processed/tweets.dict')

# Build the corpus: vectors with occurence of each word for each document
# convert tokenized documents to vectors
corpus = [dictionary.doc2bow(doc) for doc in documents]

# and save in Market Matrix format
corpora.MmCorpus.serialize('../../data/processed/tweets.mm', corpus)
