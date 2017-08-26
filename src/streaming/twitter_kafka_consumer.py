import os
import pickle

from pyspark import SparkContext
from pyspark.streaming import StreamingContext
from pyspark.streaming.kafka import KafkaUtils
from gensim.models import LdaModel
from gensim.corpora import MmCorpus, Dictionary
from src.streaming import spark_functions

os.environ['PYSPARK_SUBMIT_ARGS'] \
    = '--packages org.apache.spark:spark-streaming-kafka-0-8_2.11:2.0.2 pyspark-shell'


class TwitterKafkaConsumer(object):
    def __init__(self):
        sc = SparkContext.getOrCreate()
        sc.setLogLevel("ERROR")
        # TODO StreamingContext.getOrCreate()
        self.ssc = StreamingContext(sc, 1)  # 1 second window
        self.ssc.checkpoint("./checkpoints")

        # Load dictionary and corpus, which is needed to classify new documents (=tweets)
        dir_path = os.path.dirname(os.path.realpath(__file__))
        self.dictionary = Dictionary.load(dir_path + '/../../data/processed/tweets.dict')
        self.lda = LdaModel.load(dir_path + '/../../models/lda/gensim/tweets.lda')

        # Load sentiment model
        classifier_f = open("./../../models/naive_bayes/nltk_naive_bayes.pickle","rb")
        self.classifier = pickle.load(classifier_f)
        classifier_f.close()

    def start(self, sid):
        # ONLY USE GLOBAL FUNCTIONS!
        # Create the stream
        stream = KafkaUtils.createStream(self.ssc, 'docker:2181', "thesis-stream", {str(sid): 1})
        # Perform preprocessing on the incoming tweets
        # 1. The actual tweet is the second element in a tupel
        # 2. We just need the text
        # 3. Use the same preprocessing function as everywhere else, for consitency
        preprocessed = stream\
            .map(lambda data: data[1]) \
            .map(lambda data: data[1]) \
            .map(spark_functions.preprocess())

        # 1. Use the same tokenization function as everywhere else
        topic_model = preprocessed \
            .map(spark_functions.tokenize()) \
            .map(spark_functions.lda(dictionary=self.dictionary, model=self.lda))

        # TODO unite all these in one sparkjob
        # sentiment_model =

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

        # Emit the topics
        topic_model.foreachRDD(lambda rdd: spark_functions.emit_each('dashboard.lda-update', sid, rdd.collect()))

        # Emit all tweets for the tweets column
        # Limit to 5 tweets per window
        preprocessed.foreachRDD(lambda rdd: spark_functions.emit_each('dashboard.status-create', sid, rdd.take(5)))

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
