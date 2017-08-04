from pyspark import SparkContext
from pyspark.streaming import StreamingContext
from pyspark.streaming.kafka import KafkaUtils


# TODO rename both
class TwitterKafkaConsumer(object):
    def __init__(self, sid):
        self.interval = 5  # interval in seconds to process tweets

        self.ssc = StreamingContext(SparkContext.getOrCreate(), 10)  # 1 second window
        self.ssc.checkpoint("./checkpoints")
        self.kvs = KafkaUtils.createStream(self.ssc, 'docker:2181', "spark-streaming-consumer", {str(sid): 1})

    def listen(self):
        self.kvs.pprint()
        # TODO perform lda and send via socketio
        self.ssc.start()
        self.ssc.awaitTermination()
