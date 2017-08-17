This project is made up of 4 components that each play a part in analysing twitter sentiment,
and each have to run in a separate process.

1. Producer - Initializes the Twitter stream and connects it to Kafka
2. Queue - Using Kafka, right now just as a pub/sub message queue. Even though this is second in the pipeline, this has to be run first, otherwise the producer script will fail with nothing to stream into.
3. Consumer - Takes the messages out of the queue in batches and performs the algorithms on the data, i.e. LDA topic modeling.
4. Visualization - a web app that visualizes the outputs from the consumer-algorithm

For instructions on how to run each component, see the component's README.



To create the virtual env:
TODO
dhcp-10-176-41-248:VirtualEnvs claasmeiners$ virtualenv botstop
dhcp-10-176-41-248:VirtualEnvs claasmeiners$ source botstopper/bin/activate
(botstopper) dhcp-10-176-41-248:VirtualEnvs claasmeiners$ cd ../PycharmProjects/Botstopper/
(botstopper) dhcp-10-176-41-248:Botstopper claasmeiners$ pip3 install -U .

To start the thing up:
TODO start from beginning

from pyspark import SparkContext
from pyspark.streaming import StreamingContext
from pyspark.streaming.kafka import KafkaUtils


def take_and_print(rdd):
    for record in rdd.take(10):
        print(record)


sc = SparkContext.getOrCreate()
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


To start the Notebook Server:

Start pyspark in Notebook mode
export SPARK_HOME="/Users/claasmeiners/Library/spark/"
export PYSPARK_DRIVER_PYTHON=jupyter
export PYSPARK_DRIVER_PYTHON_OPTS="notebook"

ggf.
export PYSPARK_SUBMIT_ARGS='--packages org.mongodb.spark:mongo-spark-connector_2.10:1.1.0'