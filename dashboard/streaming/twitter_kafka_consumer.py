import os

from pyspark import SparkContext
from pyspark.streaming import StreamingContext
from pyspark.streaming.kafka import KafkaUtils

from streaming import spark_functions

os.environ['PYSPARK_SUBMIT_ARGS'] \
    = '--packages org.apache.spark:spark-streaming-kafka-0-8_2.11:2.0.2 pyspark-shell'


class TwitterKafkaConsumer(object):
    def __init__(self):
        sc = SparkContext.getOrCreate()
        sc.setLogLevel("ERROR")
        self.ssc = StreamingContext(sc, 1)  # 1 second window

    def start(self, sid):
        # ONLY USE GLOBAL FUNCTIONS!

        # Create the stream
        stream = KafkaUtils.createStream(self.ssc, 'docker:2181', "thesis-stream", {str(sid): 1})
        # Perform preprocessing on the incoming tweets
        preprocessed = stream.map(spark_functions.preprocess())
        # Perform LDA
        topic_model = preprocessed.map(spark_functions.lda())
        # Send results to client via the websocket
        topic_model.foreachRDD(lambda rdd: spark_functions.emit(rdd.collect(), sid))

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
