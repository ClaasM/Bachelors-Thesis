from pyspark import SparkContext
from pyspark.mllib.clustering import LDA
from pyspark.mllib.linalg import Vectors
from pyspark.streaming import StreamingContext
from pyspark.streaming.kafka import KafkaUtils

'''
Performs LDA on the RDD

1. Add the index as a new key and cache
2. train LDA model
3. print top three topics
'''


def lda(data):
    print(data.count())
    #data = sc.textFile("data/mllib/sample_lda_data.txt")
    parsed_data = data.map(lambda line: Vectors.dense([line.strip().split(' ')]))
    # Index documents with unique IDs
    corpus = parsed_data.zipWithIndex().map(lambda x: [x[1], x[0]]).cache()

    # Cluster the documents into three topics using LDA
    lda_model = LDA.train(corpus, k=3)

    # Output topics. Each is a distribution over words (matching word count vectors)
    # TODO stream this to a web app
    print("Learned topics (as distributions over vocab of " + str(lda_model.vocabSize()) + " words):")
    topics = lda_model.topicsMatrix()
    for topic in range(3):
        print("Topic " + str(topic) + ":")
        for word in range(0, lda_model.vocabSize()):
            print(" " + str(topics[word][topic]))


sc = SparkContext(appName="PythonTwitterStreaming")
ssc = StreamingContext(sc, 1)  # 1 second window
ssc.checkpoint("./checkpoints")
kvs = KafkaUtils.createStream(ssc, 'docker:2181', "spark-streaming-consumer", {'iphone': 1})

'''
Pre-processing:
1. Only take the value
2. Split sentences into words
3. Perform lda
'''

kvs.map(lambda x: x[1]) \
    .flatMap(lambda line: line.split(" ")) \
    .foreachRDD(lda)

ssc.start()
ssc.awaitTermination()
