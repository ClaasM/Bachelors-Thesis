# Author: Alex Perrier <alexis.perrier@gmail.com>
# License: BSD 3 clause
# Python 2.7
"""
This script loads a gensim dictionary and associated corpus
and applies an LDA model.
The documents are timelines of a 'parent' Twitter account.
They are retrieved in their tokenized version from a MongoDb database.
See also the following blog posts
* http://alexperrier.github.io/jekyll/update/2015/09/04/topic-modeling-of-twitter-followers.html
* http://alexperrier.github.io/jekyll/update/2015/09/16/segmentation_twitter_timelines_lda_vs_lsa.html
"""
from gensim import corpora, models, similarities
from pymongo import MongoClient
import time
import numpy as np

# Initialize Parameters
corpus_filename = '../../../../data/processed/tweets.mm'
dict_filename = '../../../../data/processed/tweets.dict'
lda_filename = '../../../../models/lda/gensim/tweets.lda'

# TODO try different parameters
lda_params = {'num_topics': 5, 'passes': 20, 'alpha': 0.001}

# TODO there are some sources to be recognized here:
# https://radimrehurek.com/gensim/models/ldamodel.html

# Load the corpus and Dictionary
corpus = corpora.MmCorpus(corpus_filename)
dictionary = corpora.Dictionary.load(dict_filename)

print("Running LDA with: %s  " % lda_params)
t0 = time.time()
lda = models.LdaModel(corpus, id2word=dictionary,
                      num_topics=lda_params['num_topics'],
                      passes=lda_params['passes'],
                      alpha=lda_params['alpha'])
print(time.time() - t0)
lda.print_topics()
lda.save(lda_filename)
print("lda saved in %s " % lda_filename)
