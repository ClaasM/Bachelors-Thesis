import os

from pyspark import SparkContext
from pyspark.streaming import StreamingContext
from pyspark.streaming.kafka import KafkaUtils


# TODO rename both
class TwitterKafkaConsumer(object):
    def __init__(self, sid):
        self.interval = 5  # interval in seconds to process tweets
        self.sid = sid

        # We have to explicitly include the kafka jar for the job
        os.environ['PYSPARK_SUBMIT_ARGS'] \
            = '--packages org.apache.spark:spark-streaming-kafka-0-8_2.11:2.0.2 pyspark-shell'

        self.ssc = StreamingContext(SparkContext.getOrCreate(), 1)  # 1 second window
        self.ssc.checkpoint("./checkpoints")
        self.kvs = KafkaUtils.createStream(self.ssc, 'docker:2181', "thesis-stream", {str(self.sid): 1})

    def listen(self):
        self.kvs.pprint()
        # TODO perform lda and send via socketio
        self.ssc.start()

    def await_termination(self):
        self.ssc.awaitTermination()
