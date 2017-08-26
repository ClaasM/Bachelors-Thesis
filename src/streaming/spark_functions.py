import json

from server import socketio

"""
Non-serializable functions; Don't use on execution nodes, only use on server
"""


def emit_each(event, sid, data):
    """
    Emits an array of elements, each as its own event
    :param event:
    :param sid:
    :param data:
    :return:
    """
    for element in data:
        socketio.emit(event, data=element, room=sid)


def emit(event, sid, data):
    """
    Generic emit function
    :param event:
    :param sid:
    :param data:
    :return:
    """
    socketio.emit(event, data=data, room=sid)


"""
Serializable functions to be executed on the spark execution nodes.
These are mostly factories.
Contains some utility functions to preprocess and tokenize etc. tweets.
They are here instead of the data-directory since they are also used in streaming,
because the features need to be consistent in training, testing and streaming.
"""


def preprocess():
    """
    Removes all #hashtags, @mentions and other commonly used special characters used directly in front of
    or behind valid words as well as URL's and then only keeps valid words.
    :param text: the text to be preprocessed
    :return: the preprocessed text
    """
    import re

    def _preprocess(text):
        # Remove url's
        text = re.sub(r"http\S+", "", text)
        # Remove all the other stuff
        return " ".join([word for word in re.split("[\s;,.#:-@!?'\"]", text) if word.isalpha()])

    return _preprocess


def tokenize():
    """
    Tokenization function for LDA. Used for training _and_ during streaming
    :return:
    """
    import re
    # Match http, HTTPS and @mentions
    url_pattern = re.compile(r"(?:\@|(http|https)?\://)\S+")
    from nltk.tokenize import RegexpTokenizer
    tokenizer = RegexpTokenizer(r'\w+')
    import nltk
    stoplist = set(['amp', 'get', 'got', 'hey', 'hmm', 'hoo', 'hop', 'iep', 'let', 'ooo', 'par',
                    'pdt', 'pln', 'pst', 'wha', 'yep', 'yer', 'aest', 'didn', 'nzdt', 'via',
                    'one', 'com', 'new', 'like', 'great', 'make', 'top', 'awesome', 'best',
                    'good', 'wow', 'yes', 'say', 'yay', 'would', 'thanks', 'thank', 'going',
                    'new', 'use', 'should', 'could', 'best', 'really', 'see', 'want', 'nice',
                    'while', 'know'] + nltk.corpus.stopwords.words("english"))
    from string import digits

    def _tokenize(tweet):
        # Extract tweets from text
        text = tweet['text']
        # Remove urls
        text = url_pattern.sub("", text)
        # Tokenize
        tokens = tokenizer.tokenize(text.lower())
        # Remove words with length < 3
        tokens = [token for token in tokens if len(token) > 2]
        # Remove stop words
        tokens = [token for token in tokens if token not in stoplist]
        # rm numbers only words
        tokens = [token for token in tokens if len(token.strip(digits)) == len(token)]
        # Sort words in tweet
        tokens.sort()
        return tokens

    return _tokenize


def lda(dictionary, model):
    """
    Factory for the LDA spark function
    :return:
    """

    def _lda(tokens):
        # doc2bow expects an array of unicode tokens
        doc_bow = [dictionary.doc2bow(token) for token in [tokens]]
        doc_lda = model.get_document_topics(doc_bow,
                                            minimum_probability=None,
                                            minimum_phi_value=None,
                                            per_word_topics=False)
        topics = doc_lda[0]
        topics_ret = dict()
        for topic in topics[:3]:  # Maximum 3 Topics per tweet
            topic_id = topic[0]
            topic_probability = topic[1]
            terms = model.get_topic_terms(topicid=topic_id, topn=5)
            topics_ret[topic_id] = {
                'probability': topic_probability,
                # Maximum 3 Terms per Topic
                'terms': [dictionary[term[0]] for term in terms[:3]]
            }
        return topics_ret

    return _lda


def add():
    """
    Factory for the add spark function
    :return:
    """

    def _add(new_values, last_sum):
        return sum(new_values) + (last_sum or 0)

    return _add
