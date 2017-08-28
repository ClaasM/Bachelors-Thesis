"""
This script
* Loads documents from the preprocessed sanders dataset
* Creates a dictionary and corpus that can be used to train an LDA model
"""
import csv
import random
from collections import defaultdict
from gensim import corpora

from src.streaming import spark_functions

preprocess = spark_functions.preprocessor()
tokenize = spark_functions.tokenizer()

with open('./../../data/interim/sanders_hydrated.csv') as csv_file:
    iterator = csv.reader(csv_file, delimiter=',')
    # Preprocess with the same preprocessing and tokenization function as usual
    tweets = [tokenize(preprocess(text)) for (topic, sentiment, id, text) in iterator]


# Remove words that only occur once
token_frequency = defaultdict(int)
# count all token
for tweet in tweets:
    for token in tweet:
        token_frequency[token] += 1
# keep words that occur more than once
documents = [[token for token in tweet if token_frequency[token] > 1]
             for tweet in tweets]

# Build a dictionary where for each document each word has its own id
# We stick to the default pruning settings, since they work well.
dictionary = corpora.Dictionary(documents)
dictionary.compactify()
# and save the dictionary for future use
# We use it for the topic model as well as the sentiment model.
dictionary.save('../../data/processed/tweets_sanders.dict')

# Build the corpus: vectors with occurence of each word for each document
# convert tokenized documents to vectors
corpus = [dictionary.doc2bow(doc) for doc in documents]

# and save in Market Matrix format
corpora.MmCorpus.serialize('../../data/processed/tweets_sanders.mm', corpus)
# (This is only used for the LDA topic model)
