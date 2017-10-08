from flask import session, request, Blueprint
from flask_socketio import emit
from server import socketio
from src.streaming.twitter_kafka_consumer import TwitterKafkaConsumer

from src.streaming.twitter_kafka_producer import TwitterKafkaProducer

dashboard_blueprint = Blueprint('dashboard', __name__)

def stop_pipeline():
    if 'consumer' in session:
        session['consumer'].stop()
    if 'producer' in session:
        session['producer'].stop()


@socketio.on('dashboard.update-settings')
def update(settings):
    """
    Starts or updates the pipeline
    :param settings: settings for the twitter stream and which stream to use
    :return: None
    """
    print(settings)
    try:
        if 'token' not in session:
            raise 401
        else:
            # Make sure consumer and producer are running
            # (if the user is starting the stream for the first time in this session)
            if 'consumer' not in session:
                # Start the consumer first
                consumer = TwitterKafkaConsumer()
                consumer.start(sid=str(request.sid))
                session['consumer'] = consumer
            if 'producer' not in session:
                # Then start the producer
                producer = TwitterKafkaProducer(access_token=session['token'][0],
                                                access_token_secret=session['token'][1],
                                                sid=str(request.sid))
                session['producer'] = producer

            session['producer'].update(settings)
            emit('dashboard.update-success')
    except 401:
        emit('dashboard.update-error', "Unauthorized")


@socketio.on('connect')
def handle_connect():
    print("Connected!")


@socketio.on('disconnect')
def handle_disconnect():
    stop_pipeline()
    print("Disconnected")