import os
import pickle

from gensim.corpora import Dictionary
from gensim.models import LdaModel
from pyspark import SparkContext
from pyspark.streaming import StreamingContext
from pyspark.streaming.kafka import KafkaUtils
from server import socketio
from src.streaming import spark_functions

os.environ['PYSPARK_SUBMIT_ARGS'] \
    = '--packages org.apache.spark:spark-streaming-kafka-0-8_2.11:2.0.2 pyspark-shell'


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


class TwitterKafkaConsumer(object):
    def __init__(self):
        sc = SparkContext.getOrCreate()
        sc.setLogLevel("ERROR")
        # TODO StreamingContext.getOrCreate()
        self.ssc = StreamingContext(sc, 1)  # 1 second window
        self.ssc.checkpoint("./checkpoints")

        # Load dictionary and corpus, which is needed to classify new documents (=tweets)
        dir_path = os.path.dirname(os.path.realpath(__file__))
        self.dictionary = Dictionary.load(dir_path + '/../../data/processed/tweets_stream.dict')
        self.lda_model = LdaModel.load(dir_path + '/../../models/lda/gensim/tweets_stream.lda')

        # Load sentiment model
        classifier_f = open(dir_path + "/../../models/naive_bayes/nltk_naive_bayes.pickle", "rb")
        self.sentiment_classifier = pickle.load(classifier_f)
        classifier_f.close()

    def start(self, sid):
        # ONLY USE GLOBAL FUNCTIONS!
        # Create the stream
        stream = KafkaUtils.createStream(self.ssc, 'docker:2181', "thesis-stream", {str(sid): 1})
        # Perform the analysis on each incoming element
        analyzed = stream.map(
            spark_functions.analyzer(dictionary=self.dictionary,
                                     sentiment_classifier=self.sentiment_classifier,
                                     lda_model=self.lda_model))
        # Emit each analysis result to the client to update the dashboard
        analyzed.foreachRDD(lambda rdd: emit_each('dashboard.update', sid, rdd.collect()))
        # Start the streaming
        self.ssc.start()

    def stop(self):
        self.ssc.stop()
        print("Streaming context stopped")

    def await_termination(self):
        """
        Blocking.
        This can be used during testing/in notebooks to prevent the script from terminating.
        Not needed for use on the server.
        :return:
        """
        self.ssc.awaitTermination()
