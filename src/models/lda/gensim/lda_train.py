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
TODO attribuions (also in Thesis)
"""

