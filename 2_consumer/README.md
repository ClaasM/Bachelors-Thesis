Start a shell and make sure the following environment variables are set:

`export PYSPARK_PYTHON=python3`

`export SPARK_HOME=/Users/claasmeiners/Library/spark-1.5.1-bin-hadoop2.6`

For simple word count, run:

`$SPARK_HOME/bin/spark-submit --jars jar/spark-streaming-kafka-assembly_2.10-1.5.1.jar sparkjobs/word_count.py`

For LDA topic modeling, run:

`$SPARK_HOME/bin/spark-submit --jars jar/spark-streaming-kafka-assembly_2.10-1.5.1.jar sparkjobs/word_count.py`
