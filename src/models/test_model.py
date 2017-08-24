# TODO this has to bring the tweets in about the same format as the built-in training set
def clean_split(text):
    return [word for word in text.split()
                            if 'http' not in word
                                and not word.startswith('@')
                                and not word.startswith('#')
                                and word != 'RT'
                            ]

# Evaluate classifier performance on twitter test set
import os
print(sentim_analyzer.classify(["I","hate","twitter","so","much"])) # "obj" --> objective

with open('./../../data/external/umich_sentiment_labeled.txt') as twitter_test_set_file:
    twitter_test_set = csv.reader(twitter_test_set_file, delimiter='\t')
    # Bring the data in the format expected by the evaluate-function
    evaluation_docs = [(clean_split(doc[1]), 'subj' if doc[0] == '1' else 'obj') for doc in twitter_test_set]
    #print(evaluation_docs[:10])
    evaluation_set = sentim_analyzer.apply_features(evaluation_docs)
    for key,value in sorted(sentim_analyzer.evaluate(evaluation_set).items()):
        print('{0}: {1}'.format(key, value))

# The Problem: the classifier is trained on subjectivity and objectivity, not positive/negative!