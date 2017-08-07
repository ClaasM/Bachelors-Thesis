import os

from pyspark import SparkContext
from pyspark.streaming import StreamingContext
from pyspark.streaming.kafka import KafkaUtils
import streaming.spark_functions as spark_functions


# TODO rename both
class TwitterKafkaConsumer(object):
    def __init__(self):
        self.interval = 5  # interval in seconds to process tweets

        # We have to explicitly include the kafka jar for the job
        os.environ['PYSPARK_SUBMIT_ARGS'] \
            = '--packages org.apache.spark:spark-streaming-kafka-0-8_2.11:2.0.2 pyspark-shell'

        sc = SparkContext.getOrCreate()
        sc.setLogLevel("ERROR")
        self.ssc = StreamingContext(sc, 1)  # 1 second window
        self.ssc.checkpoint("./checkpoints")

    def listen(self, sid):
        # ONLY USE GLOBAL FUNCTIONS!
        KafkaUtils.createStream(self.ssc, 'docker:2181', "thesis-stream", {str(sid): 1}) \
            .map(spark_functions.lda()) \
            .foreachRDD(lambda rdd: spark_functions.emit(rdd.collect(), sid))

        # TODO perform lda and send back to client somehow
        self.ssc.start()

    def await_termination(self):
        self.ssc.awaitTermination()
