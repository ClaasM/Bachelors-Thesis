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
        print(event, sid, element)
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
These are mostly factories
"""


def preprocess():
    def _preprocess(data):
        tweet = json.loads(data[1])  # TODO what is data[0]?

        return tweet

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
