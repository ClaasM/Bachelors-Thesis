import os

from pyspark import SparkContext
from pyspark.streaming import StreamingContext
from pyspark.streaming.kafka import KafkaUtils
from dashboard import socketio
import streaming.spark_functions as spark_functions


# TODO rename both
class TwitterKafkaConsumer(object):
    def __init__(self, sid):
        self.interval = 5  # interval in seconds to process tweets
        self.sid = sid

        # We have to explicitly include the kafka jar for the job
        os.environ['PYSPARK_SUBMIT_ARGS'] \
            = '--packages org.apache.spark:spark-streaming-kafka-0-8_2.11:2.0.2 pyspark-shell'

        sc = SparkContext.getOrCreate()
        self.ssc = StreamingContext(sc, 1)  # 1 second window
        self.ssc.checkpoint("./checkpoints")
        self.kvs = KafkaUtils.createStream(self.ssc, 'docker:2181', "thesis-stream", {str(self.sid): 1})

    def listen(self):
        # ONLY USE GLOBAL FUNCTIONS!
        sid = self.sid
        self.kvs.map(spark_functions.send_via_socket(sid)) \
            .pprint()  # This is required because we need an output operation
        # TODO perform lda and send via socketio
        self.ssc.start()

    def await_termination(self):
        self.ssc.awaitTermination()
