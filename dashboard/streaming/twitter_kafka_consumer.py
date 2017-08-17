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
        # TODO StreamingContext.getOrCreate()
        self.ssc = StreamingContext(sc, 1)  # 1 second window
        self.ssc.checkpoint("./checkpoints")

    def start(self, sid):
        # ONLY USE GLOBAL FUNCTIONS!
        # Create the stream
        stream = KafkaUtils.createStream(self.ssc, 'docker:2181', "thesis-stream", {str(sid): 1})
        # Perform preprocessing on the incoming tweets
        preprocessed = stream.map(spark_functions.preprocess())
        # TODO Perform LDA
        topic_model = preprocessed.map(spark_functions.lda())

        # TODO comment each line
        running_counts = preprocessed \
            .map(lambda tweet: tweet['text']) \
            .flatMap(lambda line: line.split(" ")) \
            .map(lambda word: (word, 1)) \
            .updateStateByKey(spark_functions.add()) \
            .transform(lambda rdd: rdd.sortBy(lambda x: x[1], False)) \
            .map(lambda tupel: {'keyword': tupel[0], 'count': tupel[1]})

        # Emit the wordcount of the top 5 keywords for the wordcount column
        running_counts.foreachRDD(lambda rdd: spark_functions.emit('dashboard.wordcount-update', sid, rdd.take(5)))

        # Emit all tweets for the tweets column
        # Limit to 5 tweets per window
        preprocessed.foreachRDD(lambda rdd: spark_functions.emit_status('dashboard.status-create', sid, rdd.take(5)))

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
