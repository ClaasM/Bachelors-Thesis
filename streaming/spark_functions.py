from dashboard import socketio

"""
Non-serializable functions; Don't use on execution nodes, only use on server
"""


def emit(rdd, sid):
    for y in rdd:
        socketio.emit('dashboard.status-create', data=y, room=sid)


"""
Serializable functions to be executed on the spark execution nodes
"""


def lda():
    def _lda(data):
        tweet = data[1]  # TODO what is data[0]?
        return tweet

    return _lda
