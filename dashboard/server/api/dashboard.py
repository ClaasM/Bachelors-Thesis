from flask import redirect, session, request, Blueprint
from server import socketio
from streaming.twitter_kafka_consumer import TwitterKafkaConsumer

from streaming.twitter_kafka_producer import TwitterKafkaProducer

dashboard_blueprint = Blueprint('dashboard', __name__)


def stop_pipeline():
    if 'consumer' in session:
        session['consumer'].stop()
    if 'producer' in session:
        session['producer'].stop()


@socketio.on('update')
def update(settings):
    """
    Starts or updates the pipeline
    :param settings: settings for the twitter stream and which stream to use
    :return: None
    """
    if 'token' not in session:
        print("Not logged in!")
        redirect('/')  # TODO this doesn't work
    else:
        # TODO update settings instead of recreating (as far as that's possible)
        stop_pipeline()
        print(settings)
        print(request.sid)
        # Start the consumer first
        consumer = TwitterKafkaConsumer()
        consumer.start(sid=str(request.sid))
        # Then start the producer
        producer = TwitterKafkaProducer(access_token=session['token'][0],
                                        access_token_secret=session['token'][1],
                                        sid=str(request.sid))
        producer.start()
        # surprisingly, this works
        session['consumer'] = consumer
        session['producer'] = producer


@socketio.on('connect')
def handle_connect():
    # TODO remove
    print("Connected!")


@socketio.on('disconnect')
def handle_disconnect():
    stop_pipeline()
    print("Disconnected")
