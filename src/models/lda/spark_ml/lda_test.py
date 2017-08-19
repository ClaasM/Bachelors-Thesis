from pyspark import SparkContext
from pyspark.ml.clustering import LocalLDAModel, LDA
from pyspark.sql import SQLContext

# Initialize
sc = SparkContext('local', 'PySPARK LDA Example')
sql_context = SQLContext(sc)

# See https://stackoverflow.com/questions/32604516/spark-mllib-lda-how-to-infer-the-topics-distribution-of-a-new-unseen-document
raise NotImplementedError
