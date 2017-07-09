Best started in Shell:

export PYSPARK_PYTHON=python3
export SPARK_HOME=/Users/claasmeiners/Library/spark-1.5.1-bin-hadoop2.6
$SPARK_HOME/bin/spark-submit --jars jar/spark-streaming-kafka-assembly_2.10-1.5.1.jar sparkjobs/trending_keywords_sparkjob.py
