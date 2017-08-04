from flask import redirect, session, request, url_for, flash, Blueprint
from dashboard import socketio
from a_producer.twitter_stream import TwitterStreamListener

dashboard_blueprint = Blueprint('dashboard', __name__)

@socketio.on('join')
def join(**kwargs):
    print("Someone joined")


@socketio.on('leave')
def leave(**kwargs):
    print("Someone left")


@socketio.on('message')
def handle_message(message):
    print('received message: ' + message)


@socketio.on('json')
def handle_json(json):
    print('handling json')


@socketio.on('connect')
def handle_connect():
    if 'token' not in session:
        print("Not logged in!")
        redirect('/')  # TODO this doesn't work
    else:
        access_token = session['token'][0]
        access_token_secret = session['token'][1]

        TwitterStreamListener(access_token=access_token, access_token_secret=access_token_secret,
                              sid=request.sid)


@socketio.on('disconnect')
def handle_connect():
    print("Someone disconnected")


@socketio.on('my event')
def handle_my_custom_event(*args, **kwargs):
    print('my event')
    # send({"test": 2}, json=True)  # send to connected client
    # emit('my response', {"test": 2})  # event name specified
    # return "Ok", 1
