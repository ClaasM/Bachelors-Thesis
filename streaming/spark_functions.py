import json

from dashboard import socketio

"""
Non-serializable functions; Don't use on execution nodes, only use on server
"""


def emit(rdd, sid):
    for status in rdd:
        socketio.emit('dashboard.status-create', data=json.loads(status), room=sid)


"""
Serializable functions to be executed on the spark execution nodes
"""


def preprocess():
    def _preprocess(data):
        tweet = data[1]  # TODO what is data[0]?
        print(tweet)
        return tweet

    return _preprocess


def lda():
    def _lda(tweet):
        print(tweet)
        return tweet

    return _lda
