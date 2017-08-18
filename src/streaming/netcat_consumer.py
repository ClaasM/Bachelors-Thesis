import os

from pyspark import SparkContext
from pyspark.streaming import StreamingContext

os.environ['PYSPARK_SUBMIT_ARGS'] \
    = '--packages org.apache.spark:spark-streaming-kafka-0-8_2.11:2.0.2 pyspark-shell'


class NetcatConsumer(object):
    """
    A class used for debugging that works with netcat instead of kafka
    """

    def __init__(self):
        sc = SparkContext.getOrCreate()
        sc.setLogLevel("ERROR")
        self.ssc = StreamingContext(sc, 1)  # 1 second window
        self.ssc.checkpoint("./checkpoints")

    def start(self, sid):
        # ONLY USE GLOBAL FUNCTIONS!
        # Create the stream
        stream = self.ssc.socketTextStream("localhost", 9999)
        # TODO test functions here
        stream.pprint()

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
