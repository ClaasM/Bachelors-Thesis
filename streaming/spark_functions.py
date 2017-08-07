"""
Serializable functions to be executed on the spark exection nodes
"""

def emit(sid, socketio):
    def _emit(rdd):
        for y in rdd:
            print("Emitting!")
            socketio.emit('dashboard.status-create', data=y, room="123")
    return _emit

def lda():
    def _lda(data):
        tweet = data[1]  # TODO what is data[0]?
        print(tweet)
        # TODO send back to webserver
        return tweet

    return _lda


def collect_and_print():
    def _collect_and_print(x):
        list = x.collect()
        for y in list:
            print(y)

    return _collect_and_print


def send_via_socket(sid, socketio):
    def _send_via_socket(x):
        list = x.collect()
        for y in list:
            socketio.emit('dashboard.status-create', data=y, room=sid)

    return _send_via_socket
