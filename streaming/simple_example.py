import os
os.environ['PYSPARK_SUBMIT_ARGS'] = '--packages org.apache.spark:spark-streaming-kafka-0-8_2.11:2.0.2 pyspark-shell'

from pyspark import SparkContext
from pyspark.streaming import StreamingContext
from pyspark.streaming.kafka import KafkaUtils
import json

sc = SparkContext.getOrCreate()
sc.setLogLevel("ERROR")
ssc = StreamingContext(sc, 60)
kafkaStream = KafkaUtils.createStream(ssc, 'docker:2181', 'spark-streaming', {'twitter':1})
kafkaStream.pprint(num=10)

ssc.start()
ssc.awaitTermination()