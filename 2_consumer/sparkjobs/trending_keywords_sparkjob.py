from pyspark import SparkContext
from pyspark.streaming import StreamingContext
from pyspark.streaming.kafka import KafkaUtils


def take_and_print(rdd):
    for record in rdd.take(10):
        print(record)


sc = SparkContext(appName="PythonTwitterStreaming")
ssc = StreamingContext(sc, 1)  # 1 second window
ssc.checkpoint("./checkpoints")
kvs = KafkaUtils.createStream(ssc, 'docker:2181', "spark-streaming-consumer", {'iphone': 1})

result = kvs.map(lambda x: x[1]) \
    .flatMap(lambda line: line.split(" ")) \
    .map(lambda word: (word, 1)) \
    .reduceByKey(lambda x, y: x + y) \
    .transform(lambda rdd: rdd.sortBy(lambda a: a[1])) \
    .foreachRDD(take_and_print)

ssc.start()
ssc.awaitTermination()

'''


'''
