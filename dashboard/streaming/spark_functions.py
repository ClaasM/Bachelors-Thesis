import json

from server import socketio

"""
Non-serializable functions; Don't use on execution nodes, only use on server
"""


def emit(event, sid, rdd):
    for status in rdd:
        #print(event, sid, json.loads(status))
        socketio.emit(event, data=json.loads(status), room=sid)


"""
Serializable functions to be executed on the spark execution nodes.
These are mostly factories
"""


def preprocess():
    def _preprocess(data):
        tweet = data[1]  # TODO what is data[0]?

        return tweet

    return _preprocess


def lda():
    """
    Factory for the LDA spark function
    :return:
    """

    def _lda(tweet):
        # print(tweet)
        return tweet

    return _lda


def add():
    """
    Factory for the add spark function
    :return:
    """

    def _add(new_values, last_sum):
        return sum(new_values) + (last_sum or 0)

    return _add
