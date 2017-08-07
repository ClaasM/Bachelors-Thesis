from flask import redirect, session, request, url_for, flash, Blueprint
from dashboard import socketio
from streaming.twitter_kafka_producer import TwitterKafkaProducer
from streaming.twitter_kafka_consumer import TwitterKafkaConsumer

dashboard_blueprint = Blueprint('dashboard', __name__)


@socketio.on('connect')
def handle_connect():
    if 'token' not in session:
        print("Not logged in!")
        redirect('/')  # TODO this doesn't work
    else:
        # Start the consumer first
        consumer = TwitterKafkaConsumer()
        consumer.listen(sid=str(request.sid))
        # Then start the producer
        producer = TwitterKafkaProducer(access_token=session['token'][0],
                                        access_token_secret=session['token'][1],
                                        sid=str(request.sid))
        producer.start()


@socketio.on('disconnect')
def handle_connect():
    # TODO handle disconnect
    print("Disconnected")
